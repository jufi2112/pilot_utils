from typing import Callable
from PyQt6.QtWidgets import QDialog
from pilot_utils.azf_trainer.ui.dialog_exam_results_base import Ui_dialog_exam_results


class AZFTrainerDialogExamResults(QDialog, Ui_dialog_exam_results):
    def __init__(self,
                 questions_correct: int,
                 questions_unanswered: int,
                 questions_total: int,
                 wrong_answers_to_watchlist_callback: Callable,
                 unanswered_questions_to_watchlist_callback: Callable,
                 pass_percentage: float = 0.75,
                 parent=None):
        """
            Params
            ------
                wrong_answers_to_watchlist_callback (Callable):
                    A function that should be called when the user selects to add all wrong answers to his watchlist
                unanswered_questions_to_watchlist_callback (Callable):
                    A function that should be called when the user selects to add all unanswered questions to his watchlist
        """
        super().__init__(parent)
        self.setupUi(self)
        percentage = round(questions_correct / questions_total, 1)
        self.label_correct.setText(f"Correct answers: {questions_correct} out of {questions_total} ({percentage*100} %)")
        cross = "<html><body><p style='color:red'>&#10008; failed</p></body></html>"
        check = "<html><body><p style='color:green'>&#10004; passed</p></body></html>"
        text = f"Exam result: {check if percentage >= pass_percentage else cross}"
        self.label_result.setText(text)
        self._set_button_unanswered_to_watchlist_text(questions_unanswered)
        self._set_button_wrong_to_watchlist_text(questions_total - questions_correct - questions_unanswered)
        self.wrong_answer_watchlist_callback = wrong_answers_to_watchlist_callback
        self.unanswered_question_watchlist_callback = unanswered_questions_to_watchlist_callback
        self.connect_signals_and_slots()


    def connect_signals_and_slots(self):
        self.button_unanswered_to_watchlist.clicked.connect(self.button_unanswered_to_watchlist_clicked_callback)
        self.button_wrong_to_watchlist.clicked.connect(self.button_wrong_to_watchlist_clicked_callback)


    def disconnect_signals_and_slots(self):
        self.button_unanswered_to_watchlist.clicked.disconnect()
        self.button_wrong_to_watchlist.clicked.disconnect()


    def _set_button_unanswered_to_watchlist_text(self, n_unanswered: int):
        self.button_unanswered_to_watchlist.setText(f"Add unanswered questions to watch list ({n_unanswered})")
        if n_unanswered == 0:
            self.button_unanswered_to_watchlist.setEnabled(False)


    def _set_button_wrong_to_watchlist_text(self, n_wrong: int):
        self.button_wrong_to_watchlist.setText(f"Add wrong answers to watch list ({n_wrong})")
        if n_wrong == 0:
            self.button_wrong_to_watchlist.setEnabled(False)


    def button_unanswered_to_watchlist_clicked_callback(self):
        self.unanswered_question_watchlist_callback()
        self.button_unanswered_to_watchlist.setEnabled(False)


    def button_wrong_to_watchlist_clicked_callback(self):
        self.wrong_answer_watchlist_callback()
        self.button_wrong_to_watchlist.setEnabled(False)
