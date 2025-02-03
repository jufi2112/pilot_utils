from pilot_utils.azf_trainer.ui.question_widget_base import Ui_question_widget
from pilot_utils.azf_trainer.ui.clickable_label import ClickableLabel
from PyQt6.QtWidgets import QWidget, QRadioButton
from functools import partial
from typing import Callable, List

class QuestionWidget(QWidget, Ui_question_widget):
    def __init__(self,
                 parent,
                 submission_callback: Callable,
                 mark_done_callback: Callable,
                 watch_callback: Callable,
                 stop_callback: Callable,
                 previous_question_callback: Callable,
                 next_question_callback: Callable):
        """
            Params
            ------
                submission_callback (Callable):
                    Function that accepts an integer (selected answer 0-3 for A-D) and returns the integer of the correct answer (0-3 for A-D)
                mark_done_callback (Callable):
                    Function that should be called if the current question gets flagged as 'done'.
                watch_callback (Callable):
                    Function that should be called if the current question gets flagged as 'watch'.
                stop_callback (Callable):
                    Function that should be called if the current training is stopped.
                previous_question_callback (Callable):
                    Function that should be called if the previous question is requested.
                next_question_callback (Callable):
                    Function that should be called if the next question is requested.
        """
        super().__init__(parent)
        self.setupUi()
        self.submission_callback = submission_callback
        self.mark_done_callback = mark_done_callback
        self.watch_callback = watch_callback
        self.stop_callback = stop_callback
        self.previous_question_callback = previous_question_callback
        self.next_question_callback = next_question_callback
        self.answer_labels: List[QRadioButton] = [self.label_answer_A, self.label_answer_B, self.label_answer_C, self.label_answer_D]
        self.answer_radio_buttons: List[ClickableLabel] = [self.radioButton_answer_A, self.radioButton_answer_B, self.radioButton_answer_C, self.radioButton_answer_D]
        self.connect_signals_and_slots()
        self.init_ui()


    def _clear_label_styles(self):
        for label in self.answer_labels:
            label.setStyleSheet("")


    def init_ui(self):
        self.button_submit.setEnabled(False)
        self._clear_label_styles()
        for rad_but in self.answer_radio_buttons:
            rad_but.setChecked(False)


    def connect_signals_and_slots(self):
        self.label_answer_A.clicked.connect(partial(self.label_question_clicked_callback, self.radioButton_answer_A))
        self.label_answer_B.clicked.connect(partial(self.label_question_clicked_callback, self.radioButton_answer_B))
        self.label_answer_C.clicked.connect(partial(self.label_question_clicked_callback, self.radioButton_answer_C))
        self.label_answer_D.clicked.connect(partial(self.label_question_clicked_callback, self.radioButton_answer_D))
        self.button_submit.clicked.connect(self.button_submit_clicked_callback)
        self.button_done.clicked.connect(self.mark_done_callback)
        self.button_watch.clicked.connect(self.watch_callback)
        self.button_home.clicked.connect(self.stop_callback)
        self.button_previous.clicked.connect(self.previous_question_callback)
        self.button_next.clicked.connect(self.next_question_callback)


    def label_question_clicked_callback(self, radioButton: QRadioButton):
        radioButton.setChecked(True)


    def radio_button_checked_callback(self):
        if self.radioButton_answer_A.isChecked() or self.radioButton_answer_B.isChecked() or self.radioButton_answer_C.isChecked() or self.radioButton_answer_D.isChecked():
            self.button_submit.setEnabled(True)
        else:
            self.button_submit.setEnabled(False)


    def button_submit_clicked_callback(self):
        selection = None
        for idx, button in enumerate(self.answer_radio_buttons):
            if button.isChecked():
                selection = idx
                break
        if selection is None:
            raise ValueError("Submit button clicked without any of the answers selected")
        correct_answer = self.submission_callback(selection)
        self._highlight_correct(selection, correct_answer)


    def fill_question(self,
                      question_text: str,
                      answer_a: str,
                      answer_b: str,
                      answer_c: str,
                      answer_d: str,
                      selected_answer: int = None,
                      correct_answer: int = None):
        self.init_ui()
        self.label_question.setText(question_text)
        for text, label in zip([answer_a, answer_b, answer_c, answer_d], self.answer_labels):
            label.setText(text)
        if selected_answer is not None and correct_answer is not None:
            self._highlight_correct(selected_answer, correct_answer)
            self.answer_radio_buttons[selected_answer].setChecked(True)
            self.button_submit.setEnabled(True)


    def _highlight_correct(self, selected: int, correct: int):
        self._clear_label_styles()
        if selected == correct:
            self.answer_labels[selected].setStyleSheet("color: green")
        else:
            self.answer_labels[selected].setStyleSheet("color: red")
            self.answer_labels[correct].setStyleSheet("color: green")
