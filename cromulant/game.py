from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel

from .ants import Ants
from .window import Window


class CircleWidget(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = QColor(*color)
        self.setFixedSize(20, 20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())


class Game:
    @staticmethod
    def update_view() -> None:
        for ant in Ants.ants:
            container = QHBoxLayout()
            circle = CircleWidget(ant.color)
            text = QLabel(ant.status)
            container.addWidget(circle)
            container.addWidget(text)
            Window.view.addLayout(container)


    @staticmethod
    def log(message: str) -> None:
        Window.log.append(message)