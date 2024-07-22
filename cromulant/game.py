from __future__ import annotations

import random

from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtWidgets import QHBoxLayout  # type: ignore
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QMouseEvent  # type: ignore
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer

from .config import Config
from .utils import Utils
from .ants import Ant
from .ants import Ants
from .window import Window
from .settings import Settings


class Method:
    merge = 0

    triumph = 1
    hit = 2

    travel = 3

    thinking_1 = 4
    thinking_2 = 5

    sentence_1 = 6
    sentence_2 = 7
    sentence_3 = 8
    sentence_4 = 9

    Opts = tuple[list[int], list[int]]

    @staticmethod
    def opts_all() -> Opts:
        opts = [
            Method.triumph,
            Method.hit,
            Method.travel,
            Method.thinking_1,
            Method.thinking_2,
            Method.sentence_1,
            Method.sentence_2,
            Method.sentence_3,
            Method.sentence_4,
        ]

        weights = [2, 2, 2, 2, 2, 3, 3, 3, 3]
        return opts, weights

    @staticmethod
    def opts_score() -> Opts:
        opts = [Method.triumph, Method.hit]
        weights = [2, 2]
        return opts, weights

    @staticmethod
    def opts_travel() -> Opts:
        opts = [Method.travel]
        weights = [2]
        return opts, weights

    @staticmethod
    def opts_thought() -> Opts:
        opts = [Method.thinking_1, Method.thinking_2]
        weights = [2, 2]
        return opts, weights

    @staticmethod
    def opts_words() -> Opts:
        opts = [
            Method.sentence_1,
            Method.sentence_2,
            Method.sentence_3,
            Method.sentence_4,
        ]

        weights = [2, 2, 2, 2]
        return opts, weights


class Game:
    timer: QTimer | None = None
    playing_song: bool = False
    merge_charge: int = 0

    @staticmethod
    def prepare() -> None:
        Game.fill()
        Game.info()
        Game.intro()

    @staticmethod
    def update(ant: Ant) -> None:
        root = QWidget()
        container = QHBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        container.setContentsMargins(0, 0, 0, 0)
        image_label = Game.get_image(ant)
        right_container = Game.make_right_container(ant)
        container.addWidget(image_label)
        container.addSpacing(Config.space_1)
        container.addWidget(right_container)
        root.setLayout(container)
        Game.add_item(root)

    @staticmethod
    def message(text: str) -> None:
        root = QWidget()
        root.setContentsMargins(0, 10, 0, 10)

        container = QHBoxLayout()
        container.setAlignment(Qt.AlignCenter)

        left_line = QFrame()
        left_line.setFrameShape(QFrame.HLine)
        left_line.setFrameShadow(QFrame.Sunken)
        left_line.setObjectName("horizontal_line")
        left_line.setFixedHeight(2)
        Window.expand_2(left_line)

        label = QLabel(text)

        right_line = QFrame()
        right_line.setFrameShape(QFrame.HLine)
        right_line.setFrameShadow(QFrame.Sunken)
        right_line.setObjectName("horizontal_line")
        right_line.setFixedHeight(2)
        Window.expand_2(right_line)

        container.addWidget(left_line)
        container.addWidget(label)
        container.addWidget(right_line)

        container.setSpacing(Config.space_1 * 2)
        root.setLayout(container)
        Game.add_item(root)

    @staticmethod
    def add_item(item: QWidget) -> None:
        from .filter import Filter

        Window.view.insertWidget(0, item)

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
    def get_image(ant: Ant) -> QLabel:
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

        mode = Settings.mode
        nums: list[int]
        weights: list[int]

        if mode == "all":
            nums, weights = Method.opts_all()
        elif mode == "score":
            nums, weights = Method.opts_score()
        elif mode == "travel":
            nums, weights = Method.opts_travel()
        elif mode == "thought":
            nums, weights = Method.opts_thought()
        elif mode == "words":
            nums, weights = Method.opts_words()
        else:
            return

        Game.merge_charge += 1

        if Game.merge_charge >= Config.merge_goal:
            nums.insert(0, Method.merge)
            weights.insert(0, 1)

        num = random.choices(nums, weights=weights, k=1)[0]

        if num == Method.merge:
            if Ants.merge():
                Game.merge_charge = 0
                return

            num = Method.sentence_4

        status = ""
        method = "normal"

        if num == Method.triumph:
            ant.triumph += 1
            method = "triumph"

        elif num == Method.hit:
            ant.hits += 1
            method = "hit"

        elif num == Method.travel:
            status = Utils.random_country([])
            method = "travel"

        elif num == Method.thinking_1:
            status = Utils.random_name([], Ants.get_names())
            method = "thinking"

        elif num == Method.thinking_2:
            status = Utils.random_emoji(3)
            method = "thinking"

        elif num == Method.sentence_1:
            status = Utils.rand_sentence.simple_sentence()

        elif num == Method.sentence_2:
            status = Utils.rand_sentence.bare_bone_sentence()

        elif num == Method.sentence_3:
            status = Utils.rand_sentence.bare_bone_with_adjective()

        elif num >= Method.sentence_4:
            status = Utils.rand_sentence.sentence()

        else:
            status = "???"

        Ants.set_status(ant, status, method)

    @staticmethod
    def fill() -> None:
        if not len(Ants.ants):
            return

        ants = sorted(Ants.ants, key=lambda ant: ant.updated)

        for ant in ants:
            Game.update(ant)

    @staticmethod
    def start_loop() -> None:
        if Game.timer:
            Game.timer.stop()

        speed = Settings.speed

        if speed == "fast":
            delay = Config.loop_delay_fast
        elif speed == "normal":
            delay = Config.loop_delay_normal
        elif speed == "slow":
            delay = Config.loop_delay_slow
        else:
            return

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
    def update_mode() -> None:
        mode = Window.mode.currentText().lower()

        if mode == Settings.mode:
            return

        Settings.set_mode(mode)
        Game.start_loop()

    @staticmethod
    def info() -> None:
        text = []

        # Non-breaking space
        nb = "\u00a0"

        if not len(Ants.ants):
            text.append("Hatch some ants")
        else:
            text.append(f"Ants:{nb}{len(Ants.ants)}")
            top = Ants.get_top()

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
        defindex = 0

        for i, opt in enumerate(opts):
            if int(opt) == Config.default_population:
                defindex = i
                break

        opts = [f"{opt} ants" for opt in opts]
        size = Window.prompt_combobox("Size of the population", opts, defindex)

        if not size:
            return

        num = int(size.split(" ")[0])

        Window.clear_view()
        Ants.populate(num)
        Window.to_top()
        Game.intro()
        Game.start_loop()

    @staticmethod
    def update_size() -> None:
        pass

    @staticmethod
    def image_action(event: QMouseEvent, ant: Ant) -> None:
        def is_terminated() -> bool:
            return ant.method == "terminated"

        if event.button() == Qt.LeftButton:
            if is_terminated():
                return

            Ants.terminate(ant)
            Game.start_loop()
        elif event.button() == Qt.MiddleButton:
            if is_terminated():
                return

            Ants.merge(ant)
            Game.start_loop()
        else:
            Game.toggle_song()

    @staticmethod
    def intro() -> None:
        version = Config.manifest["version"]
        Game.message(f"Welcome to Cromulant v{version}")
