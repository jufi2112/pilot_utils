from typing import Callable
from functools import partial
from PyQt6.QtWidgets import QDialog
from pilot_utils.azf_trainer.ui.dialog_new_training_base import Ui_new_training_dialog


class AZFTrainerDialogNewTraining(QDialog, Ui_new_training_dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_and_slots()


    def connect_signals_and_slots(self):
        self.checkBox_all_questions.toggled.connect(self.checkbox_toggled_callback)


    def disconnect_signals_and_slots(self):
        self.checkBox_all_questions.toggled.disconnect()


    def checkbox_toggled_callback(self, is_active: bool):
        if is_active:
            self.spinBox_number_questions.setEnabled(False)
        else:
            self.spinBox_number_questions.setEnabled(True)
