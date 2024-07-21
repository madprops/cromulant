from __future__ import annotations

import random

from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtWidgets import QHBoxLayout  # type: ignore
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QMouseEvent  # type: ignore
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer

from .config import Config
from .utils import Utils
from .ants import Ant
from .ants import Ants
from .window import Window
from .settings import Settings


class Game:
    timer: QTimer | None = None
    playing_song: bool = False
    last_update: int = 0

    @staticmethod
    def prepare() -> None:
        Game.initial_fill()
        Game.update_info()

    @staticmethod
    def add_update(
        ant: Ant,
    ) -> None:
        container = QHBoxLayout()
        image_label = Game.get_image(ant)
        right_container = Game.make_right_container(ant)

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
    def make_right_container(ant: Ant) -> QWidget:
        if ant.method == "hatched":
            title = "Hatched"
            message = f"{ant.name} is born"
        elif ant.method == "terminated":
            title = "Terminated"
            message = f"{ant.name} is gone"
        else:
            title = ant.name
            message = ant.get_status()

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
        ant: Ant,
    ) -> QLabel:
        if ant.method == "hatched":
            path = Config.hatched_image_path
        elif ant.method == "terminated":
            path = Config.terminated_image_path
        else:
            path = Config.status_image_path

        if ant.method == "triumph":
            color = Config.triumph_color
        elif ant.method == "hit":
            color = Config.hit_color
        else:
            color = None

        tooltip = ant.tooltip()
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

        image_label.mousePressEvent = lambda event: Game.image_action(event, ant)
        return image_label

    @staticmethod
    def get_status() -> None:
        ant = Ants.get_next()

        if not ant:
            return

        min_num = 0
        max_num = 12
        no_repeat = [0]

        num = random.randint(min_num, max_num)

        if num in no_repeat:
            if Game.last_update == num:
                num = max_num

        Game.last_update = num

        if num == min_num:
            Ants.merge()
            return

        status = ""
        method = "normal"

        if num == 1:
            ant.triumph += 1
            method = "triumph"
        elif num == 2:
            ant.hits += 1
            method = "hit"
        elif num == 3:
            status = Utils.random_name([], Ants.get_names())
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
            Game.add_update(ant)

    @staticmethod
    def start_loop() -> None:
        if Game.timer:
            Game.timer.stop()

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

    @staticmethod
    def restart() -> None:
        opts = ["25", "50", "100", "250"]
        opts = [f"{opt} ants" for opt in opts]
        size = Window.prompt_combobox("Size of the population", opts, 2)

        if not size:
            return

        num = int(size.split(" ")[0])

        Window.clear_view()
        Ants.populate(num)
        Game.start_loop()

    @staticmethod
    def update_size() -> None:
        pass

    @staticmethod
    def image_action(event: QMouseEvent, ant: Ant) -> None:
        if event.button() == Qt.LeftButton:
            Ants.terminate(ant)
        elif event.button() == Qt.MiddleButton:
            Ants.merge(ant)
        else:
            Game.toggle_song()
