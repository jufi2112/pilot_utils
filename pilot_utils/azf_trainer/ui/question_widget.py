from pilot_utils.azf_trainer.ui.question_widget_base import Ui_question_widget
from pilot_utils.azf_trainer.ui.clickable_label import ClickableLabel
from pilot_utils.azf_trainer.ui.clickable_svg import ClickableSvgWidget
from pilot_utils.azf_trainer.src import AZFQuestion
from PyQt6.QtWidgets import QWidget, QRadioButton, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap
from functools import partial
from typing import Callable, List, Dict
from enum import Enum
from pilot_utils.azf_trainer.ui import resource_rc

class AZFExerciseMode(Enum):
    UNDEFINED = "UNDEFINED"
    TRAINING = "TRAINING"
    EXAM = "EXAM"
    SHOW_HIDDEN = "HIDDEN"
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
        self._replace_placeholder_widgets()
        self._setup_ignore_submit_bookmark_grid()
        self.exercise_mode: AZFExerciseMode = exercise_mode
        if self.exercise_mode == AZFExerciseMode.UNDEFINED:
            raise ValueError("AZFQuestionWidget got undefined exercise mode")
        self.timer = None
        self.time_remaining = 30 * 60
        if self.exercise_mode != AZFExerciseMode.EXAM:
            self._hide_timer()
        else:
            self._setup_timer(self.time_remaining)
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
        self.is_bookmarked: bool = False
        self.is_ignored: bool = False
        self.connect_signals_and_slots()
        self.init_ui()
        self._adapt_bookmark_widgets(False)
        self._adapt_ignore_widgets(False)


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
        elif self.exercise_mode in [AZFExerciseMode.SHOW_BOOKMARKED, AZFExerciseMode.SHOW_HIDDEN]:
            self.button_home.setText("Exit")
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
        self.label_ignore_text.clicked.connect(self.ignore_clicked_callback)
        self.svg_widget_ignore.clicked.connect(self.ignore_clicked_callback)
        self.label_bookmark_text.clicked.connect(self.bookmark_clicked_callback)
        self.svg_widget_bookmark.clicked.connect(self.bookmark_clicked_callback)
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
        self.label_ignore_text.clicked.disconnect()
        self.svg_widget_ignore.clicked.disconnect()
        self.label_bookmark_text.clicked.disconnect()
        self.svg_widget_bookmark.clicked.disconnect()
        self.button_home.clicked.disconnect()
        self.button_previous.clicked.disconnect()
        self.button_next.clicked.disconnect()
        if self.timer is not None:
            self.timer.timeout.disconnect()
            self.button_timer_stop.clicked.disconnect()


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
                      question: AZFQuestion,
                      current_question_index: int,
                      total_questions: int,
                      is_question_ignored: bool,
                      is_question_bookmarked: bool,
                      selected_answer: int = None,
                      ):
        question_id = question.id
        question_text = question.question
        answer_a = question.answers[0].answer
        answer_b = question.answers[1].answer
        answer_c = question.answers[2].answer
        answer_d = question.answers[3].answer
        correct_answer = [idx for idx, answer in enumerate(question.answers) if answer.correct][0]
        self.init_ui()
        self.button_previous.setEnabled(current_question_index > 1)
        self.button_next.setEnabled(current_question_index < total_questions)
        self.label_question_number.setText(f"Question {current_question_index} of {total_questions} (ID: {question_id})")
        self.current_question_index = question_id
        self.label_question.setText(question_text)
        for text, label in zip([answer_a, answer_b, answer_c, answer_d], self.answer_labels):
            label.setText(text)
        self.is_ignored = is_question_ignored
        self._adapt_bookmark_widgets(is_question_bookmarked)
        self._adapt_ignore_widgets(is_question_ignored)
        self.is_bookmarked = is_question_bookmarked
        if selected_answer is not None or self.exercise_mode in [AZFExerciseMode.SHOW_BOOKMARKED, AZFExerciseMode.SHOW_HIDDEN]:
            self.answer_radio_buttons[selected_answer if selected_answer is not None else correct_answer].setChecked(True)
            if self.exercise_mode == AZFExerciseMode.EXAM and not self.exercise_finished:
                return
            self._highlight_correct(selected_answer if selected_answer is not None else correct_answer, correct_answer)
            if self.exercise_mode != AZFExerciseMode.EXAM:
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


    def ignore_clicked_callback(self):
        self.is_ignored = not self.is_ignored
        self._adapt_ignore_widgets(self.is_ignored)
        self.mark_done_callback(self.current_question_index, self.is_ignored)


    def bookmark_clicked_callback(self):
        self.is_bookmarked = not self.is_bookmarked
        self._adapt_bookmark_widgets(self.is_bookmarked)
        self.watch_callback(self.current_question_index, self.is_bookmarked)


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


    def timer_tick_callback(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.label_timer.setText(self._format_time(self.time_remaining))
            self.progressBar_timer.setValue(self.time_remaining)
        else:
            self.timer.stop()
            self.progressBar_timer.setValue(0)
            self.label_timer.setText(self._format_time(0))
            self.button_timer_stop.setEnabled(False)
            self.button_timer_stop.setText("Time's Up!")
            self.stop_callback(True)


    def timer_toggle_active_callback(self):
        if self.timer is None:
            return
        if self.timer.isActive():
            self.button_timer_stop.setText("Resume")
            self.timer.stop()
        else:
            self.button_timer_stop.setText("Pause")
            self.timer.start(1000)


    def _set_submit_button_exam_text(self):
        self.button_submit.setText(f"Unanswered questions: {40-len(self.exam_selection)}")


    def _hide_timer(self):
        self.label_timer.hide()
        self.progressBar_timer.hide()
        self.button_timer_stop.hide()


    def _setup_timer(self, time_s: int):
        self.progressBar_timer.setMaximum(time_s)
        self.progressBar_timer.setValue(time_s)
        self.label_timer.setText(self._format_time(time_s))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_tick_callback)
        self.timer.start(1000)
        self.button_timer_stop.clicked.connect(self.timer_toggle_active_callback)


    def _format_time(self, seconds: int) -> str:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"


    def _adapt_bookmark_widgets(self, is_bookmarked: bool):
        self.label_bookmark_text.setText("  Bookmark")
        if is_bookmarked:
            self.svg_widget_bookmark.load(":/icons/bookmark_filled.svg")
            #self.svg_widget_bookmark.setFixedSize(37.5, 60)
            #self.label_bookmark_text.setText("Bookmark")
        else:
            self.svg_widget_bookmark.load(":/icons/bookmark_empty.svg")
            #self.svg_widget_bookmark.setFixedSize(37.5, 60)
            #self.label_bookmark_text.setText("Bookmark")
        self.svg_widget_bookmark.setFixedSize(37.5, 60)


    def _adapt_ignore_widgets(self, is_ignored: bool):
        if is_ignored:
            self.svg_widget_ignore.load(":/icons/eye_crossed.svg")
            self.label_ignore_text.setText("  Do not show again")
            #self.svg_widget_ignore.setFixedSize(90, 40)
            #self.label_ignore_text.setText("Ignored")
        else:
            self.svg_widget_ignore.load(":/icons/eye.svg")
            self.label_ignore_text.setText("  Show again")
            #self.svg_widget_ignore.setFixedSize(90, 40)
            #self.label_ignore_text.setText("Ignore")
        self.svg_widget_ignore.setFixedSize(80, 40)


    def _replace_placeholder_widgets(self):
        layout = self.svg_widget_bookmark.parentWidget().layout()
        clickable_svg: ClickableSvgWidget = ClickableSvgWidget(":/icons/bookmark_empty.svg")
        layout.replaceWidget(self.svg_widget_bookmark, clickable_svg)
        self.svg_widget_bookmark.deleteLater()
        self.svg_widget_bookmark = clickable_svg
        layout = self.svg_widget_ignore.parentWidget().layout()
        clickable_svg: ClickableSvgWidget = ClickableSvgWidget(":/icons/eye.svg")
        layout.replaceWidget(self.svg_widget_ignore, clickable_svg)
        self.svg_widget_ignore.deleteLater()
        self.svg_widget_ignore = clickable_svg


    def _setup_ignore_submit_bookmark_grid(self):
        self.gridLayout_ignore_submit_bookmark.setColumnStretch(0, 1)
        self.gridLayout_ignore_submit_bookmark.setColumnStretch(1, 2)
        self.gridLayout_ignore_submit_bookmark.setColumnStretch(2, 1)
        self.gridLayout_ignore_submit_bookmark.setAlignment(self.horizontalLayout_ignore, Qt.AlignmentFlag.AlignLeft)
        self.gridLayout_ignore_submit_bookmark.setAlignment(self.horizontalLayout_submit, Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_ignore_submit_bookmark.setAlignment(self.horizontalLayout_bookmark, Qt.AlignmentFlag.AlignRight)
