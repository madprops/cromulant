from __future__ import annotations

import random

from PySide6.QtWidgets import QWidget  # type: ignore
from PySide6.QtGui import QColor  # type: ignore
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPaintEvent

from wonderwords import RandomSentence  # type: ignore

from .ants import Ant
from .ants import Ants
from .window import Window


class CircleWidget(QWidget):  # type: ignore
    def __init__(self, color: tuple[int, int, int]) -> None:
        super().__init__(None)
        self.color = QColor(*color)
        self.setFixedSize(20, 20)

    def paintEvent(self, event: QPaintEvent) -> None:
        print(type(event))
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())


class Game:
    @staticmethod
    def add_status(ant: Ant) -> None:
        container = QHBoxLayout()
        circle = CircleWidget(ant.color)
        text = QLabel(ant.status)
        container.addWidget(circle)
        container.addWidget(text)
        Window.view.addLayout(container)

    @staticmethod
    def log(message: str) -> None:
        Window.log.append(message)

    @staticmethod
    def get_status() -> None:
        ant = Ants.get_lazy()
        num = random.randint(1, 10)

        if num == 1:
            ant.hits += 1
            ant.status = f"Took a hit ({ant.hits} total)"
        elif num == 2:
            ant.triumph += 1
            ant.status = f"Scored a triumph ({ant.triumph} total)"
        elif num == 3:
            s = RandomSentence()
            ant.status = s.simple_sentence()
        elif (num == 4) and (len(Ants.ants) > 1):
            other = Ants.get_other(ant)
            ant.status = f"Is thinking about {other.name}"
        else:
            s = RandomSentence()
            ant.status = s.bare_bone_with_adjective()

        Game.add_status(ant)
        Ants.save()
