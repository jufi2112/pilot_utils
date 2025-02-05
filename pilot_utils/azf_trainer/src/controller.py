import json
from PyQt6.QtWidgets import QMessageBox, QDialog, QFileDialog
from pilot_utils.azf_trainer.ui.main_window import AZFTrainerMainWindow, MainPages
from pilot_utils.azf_trainer.src.model import AZFTrainerModel, QuestionFilter
from pilot_utils.azf_trainer.ui.dialog_new_training import AZFTrainerDialogNewTraining
from pilot_utils.azf_trainer.ui.question_widget import AZFQuestionWidget
from pilot_utils.azf_trainer.ui.dialog_exam_results import AZFTrainerDialogExamResults
from pilot_utils.azf_trainer.src import AZFQuestion, parse_azf_questionnaire, AZFQuestionnaire
from functools import partial
from typing import Dict
from os import path as osp

class AZFTrainingController:
    def __init__(self,
                 view: AZFTrainerMainWindow,
                 fpath_questionnaire: str,
                 fpath_done: str,
                 fpath_watched: str):
        self._view = view
        self.fpath_questionnaire = fpath_questionnaire
        self.fpath_done = fpath_done
        self.fpath_watched = fpath_watched
        self._model = None
        self._training_page: AZFQuestionWidget = None
        self.question_mode: QuestionFilter = None
        self.n_questions: int = None
        self.connect_signals_and_slots()


    def connect_signals_and_slots(self):
        self._view.button_start_training.clicked.connect(self.button_start_training_callback)
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
            with open(self.fpath_questionnaire, 'w') as file:
                json.dump(questionnaire.get_json(), file, indent=4)
            QMessageBox.information(self._view,
                                    "Question Extraction Succeeded",
                                    f"Successfully extracted {questionnaire.get_num_questions()} questions from PDF",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok
                                    )
        else:
            QMessageBox.information(self._view,
                                    "Question Extraction Failed",
                                    "Could not load the provided PDF.",
                                    QMessageBox.StandardButton.Ok,
                                    QMessageBox.StandardButton.Ok
                                    )


    def button_start_training_callback(self):
        if self._model is not None:
            raise ValueError("Local model instance is not None when start training was clicked")
        start_training_dialog = AZFTrainerDialogNewTraining(self._view)
        start_training_dialog.accepted.connect(partial(self.start_new_training_accepted_callback, start_training_dialog))
        result = start_training_dialog.exec()
        start_training_dialog.accepted.disconnect()
        start_training_dialog.disconnect_signals_and_slots()
        if result != QDialog.DialogCode.Accepted:
            return
        assert self.question_mode is not None, f"No question mode set by new training start dialog!"
        assert self.n_questions is not None, f"No n_questions set by new training start dialog!"
        self._model = AZFTrainerModel(self.n_questions,
                                      self.fpath_questionnaire,
                                      self.fpath_done,
                                      self.fpath_watched,
                                      self.question_mode)
        self._training_page = AZFQuestionWidget(parent=self._view.stackedWidget,
                                                submission_callback=self.training_submit_callback,
                                                mark_done_callback=self.training_mark_done_callback,
                                                watch_callback=self.training_mark_watched_callback,
                                                stop_callback=self.training_quit_callback,
                                                previous_question_callback=self.training_previous_question_callback,
                                                next_question_callback=self.training_next_question_callback)
        self._view.add_stacked_page(self._training_page, MainPages.PAGE_TRAINING)
        success = self.training_next_question_callback()
        if success:
            self._view.switch_main_page(MainPages.PAGE_TRAINING)


    def start_new_training_accepted_callback(self, dialog: AZFTrainerDialogNewTraining):
        if dialog.radioButton_show_all.isChecked():
            self.question_mode = QuestionFilter.ALL
        elif dialog.radioButton_done_only.isChecked():
            self.question_mode = QuestionFilter.IGNORED_ONLY
        elif dialog.radioButton_watched_only.isChecked():
            self.question_mode = QuestionFilter.WATCHED_ONLY
        else:
            self.question_mode = QuestionFilter.NOT_IGNORED
        self.n_questions = -1 if dialog.checkBox_all_questions.isChecked() else dialog.spinBox_number_questions.value()


    def training_next_question_callback(self) -> bool:
        if self._model is None or self._training_page is None:
            return False
        data, current_index, total_questions = self._model.get_next_question()
        if total_questions == 0:
            QMessageBox.information(self._view, "Training Not Possible", "No questions matched your filter criteria")
            self.training_quit_callback()
            return False
        if data is None:
            QMessageBox.information(self._view, "Training Not Possible", "Failed to load next question")
            return False
        else:
            self._send_question_to_training_page(data, current_index, total_questions)
        return True


    def training_previous_question_callback(self):
        if self._model is None or self._training_page is None:
            return False
        data, current_index, total_questions = self._model.get_previous_question()
        if total_questions == 0:
            QMessageBox.information(self._view, "Training Not Possible", "No questions matched your filter criteria")
            self.training_quit_callback()
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
                                          is_question_watched=watched,
                                          selected_answer=data['user_selection'],
                                          correct_answer=correct
                                          )


    def training_mark_done_callback(self, question_id: int, ignore: bool):
        if self._model is None:
            return
        self._model.set_ignored(question_id, ignore)


    def training_mark_watched_callback(self, question_id: int, is_watched: bool):
        if self._model is None:
            return
        self._model.add_to_watchlist(question_id, is_watched)


    def training_submit_callback(self, question_id: int, selection: int) -> int:
        if self._model is None or self._training_page is None:
            return
        correct = self._model.add_user_selection(question_id, selection)
        if self._model.all_questions_answered():
            self._training_page.all_questions_answered_action()
        return correct


    def add_wrong_answers_to_watchlist_callback(self):
        pass


    def training_quit_callback(self):
        if self._training_page is None or self._model is None:
            return
        if not self._model.all_questions_answered():
            reply = QMessageBox.question(
                self._view,
                "Confirm Stop",
                "Not all questions have been answered. Stop exam?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No |QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        n_questions, n_correct, n_unanswered = self._model.get_exam_stats()
        exam_result_dialog = AZFTrainerDialogExamResults(n_correct, n_unanswered, n_questions,
                                                            wrong_answers_to_watchlist_callback=self._model.add_wrong_answers_to_watchlist,
                                                            unanswered_questions_to_watchlist_callback=self._model.add_unanswered_to_watchlist,
                                                            pass_percentage=0.75,
                                                            parent=self._view)
        result = exam_result_dialog.exec()
        if result != QDialog.DialogCode.Accepted:
            return
        self._training_page.disconnect_signals_and_slots()
        self._training_page = None
        self._model = None
        self.question_mode = None
        self.n_questions = None
        self._view.switch_main_page(MainPages.PAGE_HOME)


    def main_window_close_callback(self, event):
        event.accept()
