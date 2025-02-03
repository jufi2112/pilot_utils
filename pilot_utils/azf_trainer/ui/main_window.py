from pilot_utils.azf_trainer.ui.main_window_base import Ui_MainWindow
from pilot_utils.azf_trainer.ui.question_widget import QuestionWidget
from PyQt6.QtWidgets import QMainWindow, QWidget
from enum import Enum

class MainPages(Enum):
    PAGE_HOME = "PAGE_HOME"
    PAGE_TRAINING = "PAGE_TRAINING"


class AZFTrainerMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.page_indices = {
            MainPages.PAGE_HOME: 0
        }


    def add_stacked_page(self, widget: QWidget, page_type: MainPages):
        index = self.stackedWidget.addWidget(widget)
        self.page_indices[page_type] = index


    def switch_main_page(self, page: MainPages):
        self.stackedWidget.setCurrentIndex(self.page_indices[page])
