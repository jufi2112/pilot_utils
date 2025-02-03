from pilot_utils.azf_trainer.ui.main_window_base import Ui_MainWindow
from pilot_utils.azf_trainer.ui.question_widget import QuestionWidget
from PyQt6.QtWidgets import QMainWindow


class AZFTrainerMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.question_widget = QuestionWidget(self.stackedWidget)
        self.stackedWidget.addWidget(self.question_widget)