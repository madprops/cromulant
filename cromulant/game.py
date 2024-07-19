from __future__ import annotations

import random
from pathlib import Path

from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap  # type: ignore

from wonderwords import RandomSentence  # type: ignore

from .config import Config
from .utils import Utils
from .ants import Ant
from .ants import Ants
from .window import Window


class Game:
    @staticmethod
    def add_status(ant: Ant) -> None:
        container = QHBoxLayout()
        image_label = Game.get_image(Config.status_image_path, ant.color)
        name = QLabel(ant.name)
        status = QLabel(ant.status)

        container.addWidget(image_label)
        container.addSpacing(Config.space_1)
        container.addWidget(name)
        container.addSpacing(Config.space_1)
        container.addWidget(status)

        Window.view.insertLayout(0, container)

    @staticmethod
    def add_message(message: str, image_path: Path) -> None:
        container = QHBoxLayout()
        image_label = Game.get_image(image_path, (255, 255, 255))
        message_label = QLabel(message)

        container.addWidget(image_label)
        container.addSpacing(Config.space_1)
        container.addWidget(message_label)

        Window.view.insertLayout(0, container)

    @staticmethod
    def get_image(image_path: Path, border_color: tuple[int, int, int]) -> QLabel:
        image_label = QLabel()
        pixmap = QPixmap(str(image_path))

        scaled_pixmap = pixmap.scaled(
            Config.image_size, pixmap.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        image_label.setPixmap(scaled_pixmap)
        image_label.setFixedSize(scaled_pixmap.size())  # Set QLabel size to match QPixmap size
        border_rgb = Utils.get_rgb(border_color)
        image_label.setStyleSheet(f"bpyside6. how do i make this start at the top. top alignedorder: 2px solid {border_rgb};")
        return image_label

    @staticmethod
    def get_status() -> None:
        num_ants = len(Ants.ants)

        if not num_ants:
            return

        ant = Ants.get_lazy()
        num = random.randint(1, 10)
        s = RandomSentence()
        status = ""

        if num == 1:
            ant.hits += 1
            status = f"Took a hit ({ant.hits} total)"
        elif num == 2:
            ant.triumph += 1
            status = f"Scored a triumph ({ant.triumph} total)"
        elif (num == 3) and (num_ants > 1):
            other = Ants.get_other(ant)
            status = f"Is thinking about {other.name}"
        elif num == 4:
            status = s.simple_sentence()
        elif num == 5:
            status = s.bare_bone_sentence()
        elif num == 6:
            status = s.bare_bone_with_adjective()
        else:
            status = s.sentence()

        Ants.set_status(ant, status)
