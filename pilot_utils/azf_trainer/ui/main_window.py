from pilot_utils.azf_trainer.ui.main_window_base import Ui_MainWindow
from pilot_utils.azf_trainer.ui.question_widget import AZFQuestionWidget
from PyQt6.QtWidgets import QMainWindow, QWidget, QMessageBox
from pilot_utils import azf_trainer
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
        self.setWindowTitle(f"AZF Trainer v. {azf_trainer.__version__}")
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
                                f"<span>AZF Trainer version {azf_trainer.__version__}<br>Copyright &#169; 2025 Julien Fischer<br>Published under GPL v3<br><br>For non-commercial distribution only<br>Find the source code <a href='https://github.com/jufi2112/pilot_utils'>here</a>",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Ok
                                )
