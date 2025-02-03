from PyQt6.QtWidgets import QDialog
from pilot_utils.azf_trainer.ui.dialog_new_training_base import Ui_new_training_dialog
from pilot_utils.azf_trainer.src.model import QuestionMode
from typing import Callable

class AZFTrainerDialogNewTraining(QDialog, Ui_new_training_dialog):
    def __init__(self, parent=None):
        """
            Params
            ------
                radioButton_callback (Callable):
                    A function that should be called when the dialog is accepted. Should accept a QuestionMode and a string that is either 'all' or an int
        """
        super().__init__(parent)
        self.setupUi(self)
        self.lineEdit_number_questions.setText("all")
        self.lineEdit_number_questions.textChanged.connect(self.lineEdit_changed_callback)

    def lineEdit_changed_callback(self, text: str):
        """Only allow 'all' or an integer"""
        if "all".startswith(text):
            return
        try:
            _ = int(text)
        except:
            self.lineEdit_number_questions.setText("")
