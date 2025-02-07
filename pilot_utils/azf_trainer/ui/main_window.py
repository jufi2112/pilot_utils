from pilot_utils.azf_trainer.ui.main_window_base import Ui_MainWindow
from pilot_utils.azf_trainer.ui.question_widget import AZFQuestionWidget
from PyQt6.QtWidgets import QMainWindow, QWidget, QMessageBox
from pilot_utils.azf_trainer import __version__
from enum import Enum
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from pilot_utils.azf_trainer.ui import resource_rc

class AZFMainPages(Enum):
    HOME = "HOME"
    EXERCISE = "EXERCISE"



class AZFTrainerMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.page_indices = {
            AZFMainPages.HOME: 0
        }
        self.button_clear_bookmarks.setIcon(QIcon(":/icons/trash.svg"))
        self.button_clear_bookmarks.setIconSize(QSize(32,32))
        self.button_clear_hidden.setIcon(QIcon(":/icons/eye.svg"))
        self.button_clear_hidden.setIconSize(QSize(48,48))
        self.connect_signals_and_slots()


    def add_stacked_page(self, widget: QWidget, page_type: AZFMainPages):
        index = self.stackedWidget.addWidget(widget)
        self.page_indices[page_type] = index


    def switch_main_page(self, page: AZFMainPages):
        self.stackedWidget.setCurrentIndex(self.page_indices[page])


    def connect_signals_and_slots(self):
        self.button_exit.clicked.connect(self.close)
        self.button_about.clicked.connect(self.button_about_clicked_callback)


    def button_about_clicked_callback(self):
        QMessageBox.information(self,
                                'About AZF Trainer',
                                f"AZF Trainer version {__version__}\n\nDeveloped by Julien Fischer\n\nFor free distribution only",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok
                                )
