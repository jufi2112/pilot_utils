from pilot_utils.azf_trainer.ui.question_widget_base import Ui_question_widget
from pilot_utils.azf_trainer.ui.clickable_label import ClickableLabel
from PyQt6.QtWidgets import QWidget, QRadioButton, QLabel
from functools import partial
from typing import Callable, List, Dict
from enum import Enum

class AZFExerciseMode(Enum):
    UNDEFINED = "UNDEFINED"
    TRAINING = "TRAINING"
    EXAM = "EXAM"
    SHOW_IGNORED = "IGNORED"
    SHOW_BOOKMARKED = "BOOKMARKED"



class AZFQuestionWidget(QWidget, Ui_question_widget):
    def __init__(self,
                 parent,
                 submission_callback: Callable,
                 mark_done_callback: Callable,
                 watch_callback: Callable,
                 stop_callback: Callable,
                 previous_question_callback: Callable,
                 next_question_callback: Callable,
                 exercise_mode: AZFExerciseMode):
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
        self.setupUi(self)
        self.exercise_mode: AZFExerciseMode = exercise_mode
        if self.exercise_mode == AZFExerciseMode.UNDEFINED:
            raise ValueError("AZFQuestionWidget got undefined exercise mode")
        self.exercise_finished = False
        # When in exam mode, store selection for each question
        self.exam_selection = {}
        self.submission_callback = submission_callback
        self.mark_done_callback = mark_done_callback
        self.watch_callback = watch_callback
        self.stop_callback = stop_callback
        self.previous_question_callback = previous_question_callback
        self.next_question_callback = next_question_callback
        self.current_question_index = -1
        self.answer_labels: List[QLabel] = [self.label_answer_A, self.label_answer_B, self.label_answer_C, self.label_answer_D]
        self.result_labels: List[QLabel] = [self.label_answer_A_result, self.label_answer_B_result, self.label_answer_C_result, self.label_answer_D_result]
        self.answer_radio_buttons: List[ClickableLabel] = [self.radioButton_answer_A, self.radioButton_answer_B, self.radioButton_answer_C, self.radioButton_answer_D]
        self.is_watched: bool = False
        self.is_ignored: bool = False
        self.connect_signals_and_slots()
        self.init_ui()


    def _clear_label_styles(self):
        for label in self.answer_labels:
            label.setStyleSheet("")
        for label in self.result_labels:
            label.setStyleSheet("")
            label.setText("")
            label.setVisible(False)


    def init_ui(self):
        self.button_submit.setEnabled(False)
        if self.exercise_mode == AZFExerciseMode.TRAINING:
            self.button_home.setText("Stop Training")
        elif self.exercise_mode == AZFExerciseMode.EXAM:
            self.button_home.setText("Stop Exam")
            self._set_submit_button_exam_text()
        # TODO: Rest
        self._clear_label_styles()
        for rad_but in self.answer_radio_buttons:
            rad_but.setAutoExclusive(False)
        for rad_but in self.answer_radio_buttons:
            rad_but.setChecked(False)
        for rad_but in self.answer_radio_buttons:
            rad_but.setAutoExclusive(True)


    def connect_signals_and_slots(self):
        self.label_answer_A.clicked.connect(partial(self.label_question_clicked_callback, self.radioButton_answer_A))
        self.label_answer_B.clicked.connect(partial(self.label_question_clicked_callback, self.radioButton_answer_B))
        self.label_answer_C.clicked.connect(partial(self.label_question_clicked_callback, self.radioButton_answer_C))
        self.label_answer_D.clicked.connect(partial(self.label_question_clicked_callback, self.radioButton_answer_D))
        self.radioButton_answer_A.toggled.connect(self.radio_button_checked_callback)
        self.radioButton_answer_B.toggled.connect(self.radio_button_checked_callback)
        self.radioButton_answer_C.toggled.connect(self.radio_button_checked_callback)
        self.radioButton_answer_D.toggled.connect(self.radio_button_checked_callback)
        self.button_submit.clicked.connect(self.button_submit_clicked_callback)
        self.button_done.clicked.connect(self.button_ignore_clicked_callback)
        self.button_watch.clicked.connect(self.button_bookmark_clicked_callback)
        self.button_home.clicked.connect(self.stop_callback)
        self.button_previous.clicked.connect(self.previous_question_callback)
        self.button_next.clicked.connect(self.next_question_callback)


    def disconnect_signals_and_slots(self):
        self.label_answer_A.clicked.disconnect()
        self.label_answer_B.clicked.disconnect()
        self.label_answer_C.clicked.disconnect()
        self.label_answer_D.clicked.disconnect()
        self.radioButton_answer_A.toggled.disconnect()
        self.radioButton_answer_B.toggled.disconnect()
        self.radioButton_answer_C.toggled.disconnect()
        self.radioButton_answer_D.toggled.disconnect()
        self.button_submit.clicked.disconnect()
        self.button_done.clicked.disconnect()
        self.button_watch.clicked.disconnect()
        self.button_home.clicked.disconnect()
        self.button_previous.clicked.disconnect()
        self.button_next.clicked.disconnect()


    def label_question_clicked_callback(self, radioButton: QRadioButton):
        radioButton.setChecked(True)


    def radio_button_checked_callback(self):
        if self.radioButton_answer_A.isChecked() or self.radioButton_answer_B.isChecked() or self.radioButton_answer_C.isChecked() or self.radioButton_answer_D.isChecked():
            if self.exercise_mode != AZFExerciseMode.EXAM:
                self.button_submit.setEnabled(True)
            else:
                selection = [idx for idx, radioButton in enumerate(self.answer_radio_buttons) if radioButton.isChecked()][0]
                self.exam_selection[self.current_question_index] = selection
                self.submission_callback(self.current_question_index, selection)
                self._set_submit_button_exam_text()
        else:
            self.button_submit.setEnabled(False)


    def button_submit_clicked_callback(self):
        if self.exercise_mode == AZFExerciseMode.EXAM:
            raise ValueError("Button submit clicked despite exam mode being active.")
        selection = None
        for idx, button in enumerate(self.answer_radio_buttons):
            if button.isChecked():
                selection = idx
                break
        if selection is None:
            raise ValueError("Submit button clicked without any of the answers selected")
        correct_answer = self.submission_callback(self.current_question_index, selection)
        self._highlight_correct(selection, correct_answer)


    def fill_question(self,
                      question_id: int,
                      current_question_index: int,
                      total_questions: int,
                      question_text: str,
                      answer_a: str,
                      answer_b: str,
                      answer_c: str,
                      answer_d: str,
                      is_question_ignored: bool,
                      is_question_watched: bool,
                      selected_answer: int = None,
                      correct_answer: int = None):
        self.init_ui()
        self.label_question_number.setText(f"Question {current_question_index} of {total_questions} (ID: {question_id})")
        self.current_question_index = question_id
        self.label_question.setText(question_text)
        for text, label in zip([answer_a, answer_b, answer_c, answer_d], self.answer_labels):
            label.setText(text)
        self.button_done.setChecked(is_question_ignored)
        self.is_ignored = is_question_ignored
        self.button_watch.setChecked(is_question_watched)
        self.is_watched = is_question_watched
        if selected_answer is not None and correct_answer is not None:
            self.answer_radio_buttons[selected_answer].setChecked(True)
            if self.exercise_mode == AZFExerciseMode.EXAM and not self.exercise_finished:
                return
            self._highlight_correct(selected_answer, correct_answer)
            self.button_submit.setEnabled(True)


    def _highlight_correct(self, selected: int, correct: int):
        if self.exercise_mode == AZFExerciseMode.EXAM and not self.exercise_finished:
            return
        self._clear_label_styles()
        if selected == correct:
            self.answer_labels[selected].setStyleSheet("color: green")
            self._set_result_label(selected, True)
        else:
            self.answer_labels[selected].setStyleSheet("color: red")
            self.answer_labels[correct].setStyleSheet("color: green")
            self._set_result_label(selected, False)
            self._set_result_label(correct, True)


    def button_ignore_clicked_callback(self):
        self.is_ignored = not self.is_ignored
        self.button_done.setChecked(self.is_ignored)
        self.mark_done_callback(self.current_question_index, self.is_ignored)


    def button_bookmark_clicked_callback(self):
        self.is_watched = not self.is_watched
        self.button_watch.setChecked(self.is_watched)
        self.watch_callback(self.current_question_index, self.is_watched)


    def _set_result_label(self, index: int, is_correct: bool):
        label: QLabel = self.result_labels[index]
        if is_correct:
            #label.setStyleSheet("color: green")
            label.setText("<html><body><p style='color:green'>&#10004;</p></body></html>")
        else:
            #label.setStyleSheet("color: red")
            label.setText("<html><body><p style='color:red'>&#10008;</p></body></html>")
        label.setVisible(True)


    def all_questions_answered_action(self):
        if self.exercise_mode == AZFExerciseMode.TRAINING:
            self.button_home.setText("Finish Training")
        elif self.exercise_mode == AZFExerciseMode.EXAM:
            self.button_home.setText("Finish Exam")
        # TODO: add text for ignored / bookmarked


    def _set_submit_button_exam_text(self):
        self.button_submit.setText(f"Unanswered questions: {40-len(self.exam_selection)}")
