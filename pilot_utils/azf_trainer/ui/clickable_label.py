from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal

class ClickableLabel(QLabel):
    """
        A clickable label
    """
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)


    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)
        self.clicked.emit()
