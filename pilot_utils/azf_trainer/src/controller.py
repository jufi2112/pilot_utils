from pilot_utils.azf_trainer.ui.main_window import AZFTrainerMainWindow, MainPages
from pilot_utils.azf_trainer.src.model import AZFTrainerModel, QuestionMode
from pilot_utils.azf_trainer.ui.dialog_new_training import AZFTrainerDialogNewTraining
from pilot_utils.azf_trainer.ui.question_widget import AZFQuestionWidget
from pilot_utils.azf_trainer.src import AZFQuestion
from functools import partial
from typing import Dict

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
        self.question_mode: QuestionMode = None
        self.n_questions: int = None
        self.connect_signals_and_slots()


    def connect_signals_and_slots(self):
        self._view.button_start_training.clicked.connect(self.button_start_training_callback)
        self._view.closeEvent = self.main_window_close_callback


    def button_start_training_callback(self):
        if self._model is not None:
            raise ValueError("Local model instance is not None when start training was clicked")
        start_training_dialog = AZFTrainerDialogNewTraining(self._view)
        start_training_dialog.accepted.connect(partial(self.start_new_training_accepted_callback, start_training_dialog))
        result = start_training_dialog.exec()
        if result == 0:
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
        self.training_next_question_callback()
        self._view.switch_main_page(MainPages.PAGE_TRAINING)


    def start_new_training_accepted_callback(self, dialog: AZFTrainerDialogNewTraining):
        if dialog.radioButton_show_all.isChecked():
            self.question_mode = QuestionMode.ALL
        elif dialog.radioButton_done_only.isChecked():
            self.question_mode = QuestionMode.DONE_ONLY
        elif dialog.radioButton_watched_only.isChecked():
            self.question_mode = QuestionMode.WATCHED_ONLY
        else:
            self.question_mode = QuestionMode.NO_DONE
        n_questions = dialog.lineEdit_number_questions.text()
        if n_questions == 'all':
            self.n_questions = -1
        else:
            try:
                self.n_questions = int(n_questions)
            except:
                raise ValueError(f"Expected n_questions to be 'all' or of type int but got {n_questions}")


    def training_next_question_callback(self):
        if self._model is None or self._training_page is None:
            return
        data = self._model.get_next_question()
        if data is None:
            # TODO: No more questions, show a corresponding message
            pass
        else:
            self._send_question_to_training_page(data)



    def training_previous_question_callback(self):
        if self._model is None or self._training_page is None:
            return
        data = self._model.get_previous_question()
        if data is None:
            # TODO: Show adequate message
            pass
        else:
            self._send_question_to_training_page(data)


    def _send_question_to_training_page(self, data: Dict):
        if self._training_page is None:
            return
        question: AZFQuestion = data['question']
        correct = [idx for idx, answer in enumerate(question.answers) if answer.correct][0]
        watched = data['watched']
        done = data['done']
        self._training_page.fill_question(question_id=question.id,
                                          question_text=question.question,
                                          answer_a=question.answers[0].answer,
                                          answer_b=question.answers[1].answer,
                                          answer_c=question.answers[2].answer,
                                          answer_d=question.answers[3].answer,
                                          is_question_done=done,
                                          is_question_watched=watched,
                                          selected_answer=data['user_selection'],
                                          correct_answer=correct
                                          )


    def training_mark_done_callback(self, question_id: int, is_done: bool):
        if self._model is None:
            return
        self._model.set_done(question_id, is_done)


    def training_mark_watched_callback(self, question_id: int, is_watched: bool):
        if self._model is None:
            return
        self._model.set_watched(question_id, is_watched)


    def training_submit_callback(self, question_id: int, selection: int) -> int:
        if self._model is None or self._training_page is None:
            return
        correct = self._model.add_user_selection(question_id, selection)
        return correct


    def training_quit_callback(self):
        if self._training_page is None:
            return
        self._training_page.disconnect_signals_and_slots()
        self._training_page = None
        self._model = None
        self._view.switch_main_page(MainPages.PAGE_HOME)


    def main_window_close_callback(self, event):
        event.accept()
