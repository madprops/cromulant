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

from .config import Config
from .utils import Utils
from .ants import Ant
from .ants import Ants
from .window import Window
from .settings import Settings


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
        elif ant.method == "travel":
            status = f"Traveling to {status}"

        tooltip = ""
        tooltip += f"Updated: {Utils.to_date(ant.updated)}"
        tooltip += f"\nCreated: {Utils.to_date(ant.created)}"
        tooltip += f"\nTriumph: {ant.triumph} | Hits: {ant.hits}"
        image_label = Game.get_image(Config.status_image_path, color, tooltip=tooltip)
        right_container = Game.make_right_container(ant.name, status)

        container.addWidget(image_label)
        container.addSpacing(Config.space_1)
        container.addWidget(right_container)
        Game.add_container(container)

    @staticmethod
    def add_message(
        title: str,
        message: str,
        image_path: Path,
        color: tuple[int, int, int] | None = None,
    ) -> None:
        container = QHBoxLayout()
        image_label = Game.get_image(image_path, color)
        right_container = Game.make_right_container(title, message)

        container.addWidget(image_label)
        container.addSpacing(Config.space_1)
        container.addWidget(right_container)
        Game.add_container(container)

    @staticmethod
    def add_container(container: QHBoxLayout) -> None:
        from .filter import Filter

        root = QWidget()
        root.setContentsMargins(0, 0, 0, 0)
        container.setContentsMargins(0, 0, 0, 0)
        root.setLayout(container)
        Window.view.insertWidget(0, root)

        while Window.view.count() > Config.max_updates:
            item = Window.view.takeAt(Window.view.count() - 1)

            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                Window.delete_layout(item.layout())

        Filter.check()

    @staticmethod
    def make_right_container(title: str, message: str) -> QWidget:
        root = QWidget()
        root.setObjectName("view_right")
        container = QVBoxLayout()
        container.setAlignment(Qt.AlignTop)

        title_label = QLabel(title)
        title_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        title_label.setStyleSheet("font-weight: bold;")
        title_label.setWordWrap(True)
        title_label.setObjectName("view_title")
        Window.expand(title_label)

        message_label = QLabel(message)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message_label.setWordWrap(True)
        message_label.setObjectName("view_message")
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
        image_label.setObjectName("view_image")
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

            style = f"""
            QLabel#view_image {{
                border: 2px solid {rgb};
            }}
            """

            image_label.setStyleSheet(style)

        if tooltip:
            image_label.setToolTip(tooltip)

        image_label.mousePressEvent = lambda event: Game.toggle_song()
        return image_label

    @staticmethod
    def get_status() -> None:
        if Ants.empty():
            return

        ant = Ants.get_next()

        if not ant:
            return

        num = random.randint(1, 10)
        status = ""
        method = "normal"

        if num == 1:
            ant.triumph += 1
            method = "triumph"
        elif num == 2:
            ant.hits += 1
            method = "hit"
        elif num == 3:
            status = Utils.random_name([])
            method = "thinking"
        elif num == 4:
            status = Utils.rand_sentence.simple_sentence()
        elif num == 5:
            status = Utils.rand_sentence.bare_bone_sentence()
        elif num == 6:
            status = Utils.rand_sentence.bare_bone_with_adjective()
        elif num == 7:
            status = Utils.random_emoji(3)
            method = "thinking"
        elif num == 8:
            status = Utils.random_country([])
            method = "travel"
        else:
            status = Utils.rand_sentence.sentence()

        Ants.set_status(ant, status, method)

    @staticmethod
    def initial_fill() -> None:
        if not len(Ants.ants):
            return

        ants = sorted(Ants.ants, key=lambda ant: ant.updated)

        for ant in ants:
            if ant.status or ant.method:
                Game.add_status(ant)

    @staticmethod
    def start_loop() -> None:
        speed = Settings.speed

        if speed == "fast":
            delay = Config.loop_delay_fast
        elif speed == "slow":
            delay = Config.loop_delay_slow
        else:
            delay = Config.loop_delay_normal

        Game.timer = QTimer()
        Game.timer.timeout.connect(Game.get_status)
        Game.timer.start(delay)

    @staticmethod
    def update_speed() -> None:
        speed = Window.speed.currentText().lower()

        if speed == Settings.speed:
            return

        Settings.set_speed(speed)
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
            top = Ants.get_top_ant()

            if top:
                ant = top[0]
                score = top[1]
                text.append(f"Top:{nb}{ant.name} ({score})")

        Window.info.setText(Config.info_separator.join(text))
        Window.info.adjustSize()

    @staticmethod
    def toggle_song() -> None:
        if Game.playing_song:
            Window.stop_audio()
            Game.playing_song = False
        else:
            path = str(Config.song_path)

            def on_stop() -> None:
                Game.playing_song = False

            Window.play_audio(path, on_stop)
            Game.playing_song = True
