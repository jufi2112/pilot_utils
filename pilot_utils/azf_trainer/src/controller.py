import json
from PyQt6.QtWidgets import QMessageBox, QDialog, QFileDialog
from pilot_utils.azf_trainer.ui.main_window import AZFTrainerMainWindow, AZFMainPages
from pilot_utils.azf_trainer.src.model import AZFTrainerModel, QuestionFilter
from pilot_utils.azf_trainer.ui.dialog_new_training import AZFTrainerDialogNewTraining
from pilot_utils.azf_trainer.ui.question_widget import AZFQuestionWidget, AZFExerciseMode
from pilot_utils.azf_trainer.ui.dialog_exam_results import AZFTrainerDialogExamResults
from pilot_utils.azf_trainer.src import AZFQuestion, parse_azf_questionnaire, AZFQuestionnaire
from functools import partial
from typing import Dict
from os import path as osp
import os

class AZFTrainingController:
    def __init__(self,
                 view: AZFTrainerMainWindow,
                 fpath_questionnaire: str,
                 fpath_ignored: str,
                 fpath_bookmarked: str):
        self._view = view
        self.fpath_questionnaire = fpath_questionnaire
        self.fpath_ignored = fpath_ignored
        self.fpath_bookmarked = fpath_bookmarked
        self._update_home_page_button_states()
        self._model = None
        self._training_page: AZFQuestionWidget = None
        self.question_filter: QuestionFilter = None
        self.n_questions: int = None
        self.exercise_mode: AZFExerciseMode = AZFExerciseMode.UNDEFINED
        self.connect_signals_and_slots()


    def connect_signals_and_slots(self):
        self._view.button_start_training.clicked.connect(self.button_start_training_clicked_callback)
        self._view.button_start_exam.clicked.connect(self.button_start_exam_clicked_callback)
        self._view.button_extract_questions.clicked.connect(self.button_extract_questions_clicked_callback)
        self._view.closeEvent = self.main_window_close_callback


    def button_extract_questions_clicked_callback(self):
        if osp.exists(self.fpath_questionnaire):
            reply = QMessageBox.question(
                self._view,
                'Confirm Overwrite',
                'There already is a file that contains extracted questions.\nDo you want to continue and overwrite these questions?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        file_name, active_filter = QFileDialog.getOpenFileName(self._view,
                                                               "Select Questionnaire PDF",
                                                               "",
                                                               "PDF Files (*.pdf)"
                                                               )
        if osp.isfile(file_name) and osp.splitext(file_name)[1].lower() == '.pdf':
            # Valid file
            questionnaire: AZFQuestionnaire = parse_azf_questionnaire(file_name)
            os.makedirs(osp.dirname(self.fpath_questionnaire), exist_ok=True)
            with open(self.fpath_questionnaire, 'w') as file:
                json.dump(questionnaire.get_json(), file, indent=4)
            QMessageBox.information(self._view,
                                    "Question Extraction Succeeded",
                                    f"Successfully extracted {questionnaire.get_num_questions()} questions from PDF",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok
                                    )
            self._update_home_page_button_states()
        else:
            QMessageBox.information(self._view,
                                    "Question Extraction Failed",
                                    "Could not load the provided PDF.",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok
                                    )


    def button_start_training_clicked_callback(self):
        if self._model is not None:
            raise ValueError("Local model instance is not None when start training was clicked")
        start_training_dialog = AZFTrainerDialogNewTraining(self._view)
        start_training_dialog.accepted.connect(partial(self.start_new_training_accepted_callback, start_training_dialog))
        result = start_training_dialog.exec()
        start_training_dialog.accepted.disconnect()
        start_training_dialog.disconnect_signals_and_slots()
        if result != QDialog.DialogCode.Accepted:
            return
        assert self.question_filter is not None, f"No question mode set by new training start dialog!"
        assert self.n_questions is not None, f"No n_questions set by new training start dialog!"
        self._model = AZFTrainerModel(self.n_questions,
                                      self.fpath_questionnaire,
                                      self.fpath_ignored,
                                      self.fpath_bookmarked,
                                      self.question_filter
                                      )
        self.exercise_mode = AZFExerciseMode.TRAINING
        self._training_page = AZFQuestionWidget(parent=self._view.stackedWidget,
                                                submission_callback=self.exercise_submit_callback,
                                                mark_done_callback=self.exercise_mark_ignored_callback,
                                                watch_callback=self.exercise_bookmark_callback,
                                                stop_callback=self.exercise_quit_callback,
                                                previous_question_callback=self.exercise_previous_question_callback,
                                                next_question_callback=self.exercise_next_question_callback,
                                                exercise_mode=self.exercise_mode
                                                )
        success = self.exercise_next_question_callback()
        if success:
            self._view.add_stacked_page(self._training_page, AZFMainPages.EXERCISE)
            self._view.switch_main_page(AZFMainPages.EXERCISE)


    def button_start_exam_clicked_callback(self):
        if self._model is not None:
            raise ValueError("Local model instance is not None when start exam was clicked")
        self.question_filter = QuestionFilter.ALL
        self.n_questions = 40
        self.exercise_mode = AZFExerciseMode.EXAM
        self._model = AZFTrainerModel(self.n_questions,
                                      self.fpath_questionnaire,
                                      self.fpath_ignored,
                                      self.fpath_bookmarked,
                                      self.question_filter
                                      )
        self._training_page = AZFQuestionWidget(parent=self._view.stackedWidget,
                                                submission_callback=self.exercise_submit_callback,
                                                mark_done_callback=self.exercise_mark_ignored_callback,
                                                watch_callback=self.exercise_bookmark_callback,
                                                stop_callback=self.exercise_quit_callback,
                                                previous_question_callback=self.exercise_previous_question_callback,
                                                next_question_callback=self.exercise_next_question_callback,
                                                exercise_mode=self.exercise_mode
                                                )
        success = self.exercise_next_question_callback()
        if success:
            self._view.add_stacked_page(self._training_page, AZFMainPages.EXERCISE)
            self._view.switch_main_page(AZFMainPages.EXERCISE)


    def start_new_training_accepted_callback(self, dialog: AZFTrainerDialogNewTraining):
        if dialog.radioButton_show_all.isChecked():
            self.question_filter = QuestionFilter.ALL
        elif dialog.radioButton_done_only.isChecked():
            self.question_filter = QuestionFilter.IGNORED_ONLY
        elif dialog.radioButton_watched_only.isChecked():
            self.question_filter = QuestionFilter.WATCHED_ONLY
        else:
            self.question_filter = QuestionFilter.NOT_IGNORED
        self.n_questions = -1 if dialog.checkBox_all_questions.isChecked() else dialog.spinBox_number_questions.value()


    def exercise_next_question_callback(self) -> bool:
        if self._model is None or self._training_page is None:
            return False
        data, current_index, total_questions = self._model.get_next_question()
        if total_questions == 0:
            QMessageBox.information(self._view, "Training Not Possible", "No questions matched your filter criteria")
            self.exercise_quit_callback()
            return False
        if data is None:
            QMessageBox.information(self._view, "Training Not Possible", "Failed to load next question")
            return False
        else:
            self._send_question_to_training_page(data, current_index, total_questions)
        return True


    def exercise_previous_question_callback(self):
        if self._model is None or self._training_page is None:
            return False
        data, current_index, total_questions = self._model.get_previous_question()
        if total_questions == 0:
            QMessageBox.information(self._view, "Training Not Possible", "No questions matched your filter criteria")
            self.exercise_quit_callback()
            return False
        if data is None:
            QMessageBox.information(self._view, "Training Not Possible", "Failed to load previous question")
            return False
        else:
            self._send_question_to_training_page(data, current_index, total_questions)
        return True


    def _send_question_to_training_page(self, data: Dict, current_index: int, total_questions: int):
        if self._training_page is None:
            return
        # TODO: put this logic into question_widget?
        self._training_page.button_previous.setEnabled(current_index > 1)
        self._training_page.button_next.setEnabled(current_index < total_questions)
        question: AZFQuestion = data['question']
        correct = [idx for idx, answer in enumerate(question.answers) if answer.correct][0]
        watched = data['watched']
        ignored = data['ignored']
        self._training_page.fill_question(question_id=question.id,
                                          current_question_index=current_index,
                                          total_questions=total_questions,
                                          question_text=question.question,
                                          answer_a=question.answers[0].answer,
                                          answer_b=question.answers[1].answer,
                                          answer_c=question.answers[2].answer,
                                          answer_d=question.answers[3].answer,
                                          is_question_ignored=ignored,
                                          is_question_bookmarked=watched,
                                          selected_answer=data['user_selection'],
                                          correct_answer=correct
                                          )


    def exercise_mark_ignored_callback(self, question_id: int, ignore: bool):
        if self._model is None:
            return
        self._model.set_ignored(question_id, ignore)


    def exercise_bookmark_callback(self, question_id: int, is_watched: bool):
        if self._model is None:
            return
        self._model.add_to_watchlist(question_id, is_watched)


    def exercise_submit_callback(self, question_id: int, selection: int) -> int:
        if self._model is None or self._training_page is None:
            return
        correct = self._model.add_user_selection(question_id, selection)
        if self._model.all_questions_answered():
            self._training_page.all_questions_answered_action()
        return correct


    def add_wrong_answers_to_watchlist_callback(self):
        pass


    def exercise_quit_callback(self, force_end: bool = False):
        if self._training_page is None or self._model is None:
            return
        if not self._model.all_questions_answered() and not force_end:
            exercise_name = "<undefined>"
            if self.exercise_mode == AZFExerciseMode.TRAINING:
                exercise_name = "training"
            elif self.exercise_mode == AZFExerciseMode.EXAM:
                exercise_name = "exam"
            # TODO: add handling of bookmarked / ignored (no confirmation for not-answered questions)
            reply = QMessageBox.question(
                self._view,
                "Confirm Stop",
                f"Not all questions have been answered. Stop {exercise_name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No |QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        if self._training_page.timer is not None:
            self._training_page.timer.stop()
            self._training_page.button_timer_stop.setText("Exam Over")
            self._training_page.button_timer_stop.setEnabled(False)
        n_questions, n_correct, n_unanswered = self._model.get_exam_stats()
        exam_result_dialog = AZFTrainerDialogExamResults(n_correct, n_unanswered, n_questions,
                                                         wrong_answers_to_watchlist_callback=self._model.add_wrong_answers_to_watchlist,
                                                         unanswered_questions_to_watchlist_callback=self._model.add_unanswered_to_watchlist,
                                                         exercise_mode=self.exercise_mode, pass_percentage=0.75,
                                                         parent=self._view
                                                         )
        result = exam_result_dialog.exec()
        if result != QDialog.DialogCode.Accepted:
            self._training_page.exercise_finished = True
            return
        self._update_home_page_button_states()
        self._view.switch_main_page(AZFMainPages.HOME)
        self._view.stackedWidget.removeWidget(self._training_page)
        # TODO: Alternative: self._training_page.deleteLater()
        self._training_page.disconnect_signals_and_slots()
        self._training_page = None
        self._model = None
        self.question_filter = None
        self.n_questions = None
        self.exercise_mode = AZFExerciseMode.UNDEFINED


    def main_window_close_callback(self, event):
        event.accept()


    def _update_home_page_button_states(self):
        if self._view is None:
            return
        self._view.button_start_training.setEnabled(osp.exists(self.fpath_questionnaire))
        self._view.button_start_exam.setEnabled(osp.exists(self.fpath_questionnaire))
        self._view.button_show_watched.setEnabled(osp.exists(self.fpath_bookmarked))
        self._view.button_show_done.setEnabled(osp.exists(self.fpath_ignored))
