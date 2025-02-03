from PyQt6.QtWidgets import QDialog
from pilot_utils.azf_trainer.ui.dialog_new_training_base import Ui_new_training_dialog
from pilot_utils.azf_trainer.src.model import QuestionMode
from typing import Callable

class AZFTrainerDialogNewTraining(QDialog, Ui_new_training_dialog):
    def __init__(self, accept_callback: Callable, parent=None):
        """
            Params
            ------
                radioButton_callback (Callable):
                    A function that should be called when the dialog is accepted
        """
        super().__init__(parent)
        self.accept_callback = accept_callback
        self.setupUi(self)
        self.connect_signals_and_slots()


    def connect_signals_and_slots(self):
        self.button_start.clicked.connect(self.button_start_clicked_callback)


    def button_start_clicked_callback(self):
        mode = QuestionMode.NO_DONE
        if self.radioButton_default.isChecked():
            mode = QuestionMode.NO_DONE
        elif self.radioButton_show_all.isChecked():
            mode = QuestionMode.ALL
        elif self.radioButton_done_only:
            mode = QuestionMode.DONE_ONLY
        elif self.radioButton_watched_only.isChecked():
            mode = QuestionMode.WATCHED_ONLY
        self.accept_callback(mode)
        self.accept()
