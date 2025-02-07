from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import pyqtSignal, Qt

class ClickableSvgWidget(QSvgWidget):
    clicked = pyqtSignal()


    def __init__(self, svg_path, parent=None):
        super().__init__(parent)
        self.load(svg_path)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)
