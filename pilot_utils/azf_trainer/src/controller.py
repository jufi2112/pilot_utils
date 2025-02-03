from pilot_utils.azf_trainer.ui.main_window import AZFTrainerMainWindow
from pilot_utils.azf_trainer.src.controller import AZFTrainingController

class AZFTrainingController:
    def __init__(self, view: AZFTrainerMainWindow):
        self._view = view
