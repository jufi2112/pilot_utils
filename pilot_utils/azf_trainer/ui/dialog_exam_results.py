from typing import Callable
from PyQt6.QtWidgets import QDialog
from pilot_utils.azf_trainer.ui.dialog_exam_results_base import Ui_dialog_exam_results
from pilot_utils.azf_trainer.ui.question_widget import AZFExerciseMode


class AZFTrainerDialogExamResults(QDialog, Ui_dialog_exam_results):
    def __init__(self,
                 questions_correct: int,
                 questions_unanswered: int,
                 questions_total: int,
                 wrong_answers_to_watchlist_callback: Callable,
                 unanswered_questions_to_watchlist_callback: Callable,
                 hide_correct_questions_callback: Callable,
                 exercise_mode: AZFExerciseMode,
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
        percentage = round((questions_correct / questions_total)*100, 1)
        self.label_correct.setText(f"Correct answers: {questions_correct} out of {questions_total} ({percentage} %)")
        cross = "<span style='color:red'>&#10008; failed</span>"
        check = "<span style='color:green'>&#10004; passed</span>"
        exercise_name = "<undefined>"
        if exercise_mode == AZFExerciseMode.TRAINING:
            exercise_name = "Training"
        elif exercise_mode == AZFExerciseMode.EXAM:
            exercise_name = "Exam"
        text = f"{exercise_name} result: {check if percentage >= (pass_percentage*100) else cross}"
        self.label_result.setText(text)
        self._set_button_unanswered_to_watchlist_text(questions_unanswered)
        self._set_button_wrong_to_watchlist_text(questions_total - questions_correct - questions_unanswered)
        self._set_button_hide_correct_text(questions_correct)
        self.wrong_answer_watchlist_callback = wrong_answers_to_watchlist_callback
        self.unanswered_question_watchlist_callback = unanswered_questions_to_watchlist_callback
        self.hide_correct_questions_callback = hide_correct_questions_callback
        self.connect_signals_and_slots()


    def connect_signals_and_slots(self):
        self.button_unanswered_to_watchlist.clicked.connect(self.button_unanswered_to_watchlist_clicked_callback)
        self.button_wrong_to_watchlist.clicked.connect(self.button_wrong_to_watchlist_clicked_callback)
        self.button_hide_correct.clicked.connect(self.button_hide_correct_clicked_callback)


    def disconnect_signals_and_slots(self):
        self.button_unanswered_to_watchlist.clicked.disconnect()
        self.button_wrong_to_watchlist.clicked.disconnect()


    def _set_button_unanswered_to_watchlist_text(self, n_unanswered: int):
        self.button_unanswered_to_watchlist.setText(f"Add bookmark to unanswered questions ({n_unanswered})")
        if n_unanswered == 0:
            self.button_unanswered_to_watchlist.setEnabled(False)


    def _set_button_wrong_to_watchlist_text(self, n_wrong: int):
        self.button_wrong_to_watchlist.setText(f"Add bookmark to wrong answers ({n_wrong})")
        if n_wrong == 0:
            self.button_wrong_to_watchlist.setEnabled(False)


    def _set_button_hide_correct_text(self, n_correct: int):
        self.button_hide_correct.setText(f"Hide correctly answered questions ({n_correct})")
        if n_correct == 0:
            self.button_hide_correct.setEnabled(False)


    def button_unanswered_to_watchlist_clicked_callback(self):
        self.unanswered_question_watchlist_callback()
        self.button_unanswered_to_watchlist.setEnabled(False)


    def button_wrong_to_watchlist_clicked_callback(self):
        self.wrong_answer_watchlist_callback()
        self.button_wrong_to_watchlist.setEnabled(False)


    def button_hide_correct_clicked_callback(self):
        self.hide_correct_questions_callback()
        self.button_hide_correct.setEnabled(False)
