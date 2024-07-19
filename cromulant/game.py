from __future__ import annotations

import random
from pathlib import Path

from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtWidgets import QHBoxLayout  # type: ignore
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap  # type: ignore
from PySide6.QtCore import QTimer

from wonderwords import RandomSentence  # type: ignore

from .config import Config
from .utils import Utils
from .ants import Ant
from .ants import Ants
from .window import Window


class Game:
    timer: QTimer

    @staticmethod
    def prepare() -> None:
        Game.initial_fill()
        Game.update_info()

    @staticmethod
    def add_status(ant: Ant) -> None:
        container = QHBoxLayout()
        image_label = Game.get_image(Config.status_image_path, ant.color)
        right_container = Game.make_right_container(ant.name, ant.status)

        container.addWidget(image_label)
        container.addSpacing(Config.space_1)
        container.addWidget(right_container)
        Game.add_view_container(container)

    @staticmethod
    def add_message(title: str, message: str, image_path: Path) -> None:
        container = QHBoxLayout()
        image_label = Game.get_image(image_path, (255, 255, 255))
        right_container = Game.make_right_container(title, message)

        container.addWidget(image_label)
        container.addSpacing(Config.space_1)
        container.addWidget(right_container)
        Game.add_view_container(container)

    @staticmethod
    def add_view_container(container: QHBoxLayout) -> None:
        Window.view.insertLayout(0, container)

        while Window.view.count() > Config.max_messages:
            item = Window.view.takeAt(Window.view.count() - 1)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                Window.delete_layout(item.layout())

    @staticmethod
    def make_right_container(title: str, message: str) -> QWidget:
        root = QWidget()
        container = QVBoxLayout()
        container.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        title_label.setWordWrap(True)
        Window.expand(title_label)

        message_label = QLabel(message)
        message_label.setWordWrap(True)
        Window.expand(message_label)

        container.addWidget(title_label)
        container.addWidget(message_label)
        root.setLayout(container)

        return root

    @staticmethod
    def get_image(image_path: Path, border_color: tuple[int, int, int]) -> QLabel:
        image_label = QLabel()
        pixmap = QPixmap(str(image_path))

        scaled_pixmap = pixmap.scaled(
            Config.image_size,
            pixmap.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        image_label.setPixmap(scaled_pixmap)

        image_label.setFixedSize(scaled_pixmap.size())

        border_rgb = Utils.get_rgb(border_color)

        image_label.setStyleSheet(
            f"bpyside6. how do i make this start at the top. top alignedorder: 2px solid {border_rgb};"
        )

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
            ant.triumph += 1
            status = f"😀 Scored a triumph ({ant.triumph} total)"
        elif num == 2:
            ant.hits += 1
            status = f"🎃 Took a hit ({ant.hits} total)"
        elif (num == 3) and (num_ants > 1):
            other = Ants.get_other(ant)
            status = f"🫠 Is thinking about {other.name}"
        elif num == 4:
            status = s.simple_sentence()
        elif num == 5:
            status = s.bare_bone_sentence()
        elif num == 6:
            status = s.bare_bone_with_adjective()
        else:
            status = s.sentence()

        Ants.set_status(ant, status)

    @staticmethod
    def initial_fill() -> None:
        if not len(Ants.ants):
            return

        ants = sorted(Ants.ants, key=lambda ant: ant.updated)

        for ant in ants:
            if ant.status:
                Game.add_status(ant)

    @staticmethod
    def start_loop() -> None:
        speed = Window.speed.currentText()

        if speed == "Fast":
            delay = Config.loop_delay_fast
        elif speed == "Normal":
            delay = Config.loop_delay_normal
        else:
            delay = Config.loop_delay_slow

        Game.timer = QTimer()
        Game.timer.timeout.connect(Game.get_status)
        Game.timer.start(delay)

    @staticmethod
    def update_speed() -> None:
        Game.timer.stop()
        Game.start_loop()

    @staticmethod
    def update_info() -> None:
        text = []

        # Non-breaking space
        nb = "\u00a0"

        if not len(Ants.ants):
            text.append("Hatch some ants")
        else:
            text.append(f"Ants:{nb}{len(Ants.ants)}")
            triumph = Ants.most_triumph()

            if triumph:
                text.append(f"Triumph:{nb}{triumph.name}")

        Window.info.setText(Config.info_separator.join(text))
        Window.info.adjustSize()
