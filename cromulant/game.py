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
    playing_song: bool = False

    @staticmethod
    def prepare() -> None:
        Game.initial_fill()
        Game.update_info()

    @staticmethod
    def add_status(ant: Ant) -> None:
        container = QHBoxLayout()
        status = ant.status
        color = None

        if ant.method == "triumph":
            total = f"({ant.triumph} total)"
            status = f"{Config.triumph_icon} {Config.triumph_message} {total}"
            color = Config.triumph_color
        elif ant.method == "hit":
            total = f"({ant.hits} total)"
            status = f"{Config.hit_icon} {Config.hit_message} {total}"
            color = Config.hit_color
        elif ant.method == "thinking":
            status = f"Thinking about {status}"

        tooltip = Utils.to_date(ant.updated)
        image_label = Game.get_image(Config.status_image_path, color, tooltip=tooltip)
        right_container = Game.make_right_container(ant.name, status)

        container.addWidget(image_label)
        container.addSpacing(Config.space_1)
        container.addWidget(right_container)
        Game.add_view_container(container)

    @staticmethod
    def add_message(
        title: str,
        message: str,
        image_path: Path,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        container = QHBoxLayout()
        image_label = Game.get_image(image_path, color)
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
        container.setAlignment(Qt.AlignTop)

        title_label = QLabel(title)
        title_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        title_label.setStyleSheet("font-weight: bold;")
        title_label.setWordWrap(True)
        Window.expand(title_label)

        message_label = QLabel(message)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message_label.setWordWrap(True)
        Window.expand(message_label)

        container.addWidget(title_label)
        container.addWidget(message_label)
        root.setLayout(container)

        return root

    @staticmethod
    def get_image(
        path: Path, color: tuple[int, int, int] | None = None, tooltip: str = ""
    ) -> QLabel:
        image_label = QLabel()
        pixmap = QPixmap(str(path))

        scaled_pixmap = pixmap.scaled(
            Config.image_size,
            pixmap.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        image_label.setPixmap(scaled_pixmap)
        image_label.setFixedSize(scaled_pixmap.size())

        if color:
            rgb = Utils.get_rgb(color)
            image_label.setStyleSheet(f"border: 2px solid {rgb};")

        if tooltip:
            image_label.setToolTip(tooltip)

        image_label.mousePressEvent = lambda event: Game.toggle_song()
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
        method = "normal"

        if num == 1:
            ant.triumph += 1
            method = "triumph"
        elif num == 2:
            ant.hits += 1
            method = "hit"
        elif (num == 3) and (num_ants > 1):
            other = Ants.get_other(ant)
            status = other.name
            method = "thinking"
        elif num == 4:
            status = s.simple_sentence()
        elif num == 5:
            status = s.bare_bone_sentence()
        elif num == 6:
            status = s.bare_bone_with_adjective()
        elif num == 7:
            status = Utils.get_random_emoji(3)
            method = "thinking"
        else:
            status = s.sentence()

        Ants.set_status(ant, status, method)

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

    @staticmethod
    def toggle_song() -> None:
        if Game.playing_song:
            Window.stop_audio()
        else:
            path = str(Config.song_path)
            Window.play_audio(path)

        Game.playing_song = not Game.playing_song
