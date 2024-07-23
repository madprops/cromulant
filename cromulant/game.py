from __future__ import annotations

import random

from PySide6.QtWidgets import QHBoxLayout  # type: ignore
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QCursor  # type: ignore
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QAction
from PySide6.QtCore import QTimer  # type: ignore
from PySide6.QtCore import Qt

from .config import Config
from .utils import Utils
from .ants import Ant
from .ants import Ants
from .window import Window
from .settings import Settings


class Opt:
    def __init__(self, value: int, weight: int) -> None:
        self.value = value
        self.weight = weight


class Method:
    merge = Opt(0, 1)
    triumph = Opt(1, 2)
    hit = Opt(2, 2)
    travel = Opt(3, 2)
    thinking_1 = Opt(4, 2)
    thinking_2 = Opt(5, 2)
    sentence_1 = Opt(6, 3)
    sentence_2 = Opt(7, 3)
    sentence_3 = Opt(8, 3)
    sentence_4 = Opt(9, 3)

    @staticmethod
    def opts_score() -> list[Opt]:
        return [Method.triumph, Method.hit]

    @staticmethod
    def opts_travel() -> list[Opt]:
        return [Method.travel]

    @staticmethod
    def opts_thought() -> list[Opt]:
        return [Method.thinking_1, Method.thinking_2]

    @staticmethod
    def opts_words() -> list[Opt]:
        return [
            Method.sentence_1,
            Method.sentence_2,
            Method.sentence_3,
            Method.sentence_4,
        ]


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

        opts: list[Opt] = []

        if Settings.score_enabled:
            opts.extend(Method.opts_score())

        if Settings.travel_enabled:
            opts.extend(Method.opts_travel())

        if Settings.think_enabled:
            opts.extend(Method.opts_thought())

        if Settings.words_enabled:
            opts.extend(Method.opts_words())

        if not opts:
            return

        values = [opt.value for opt in opts]
        weights = [opt.weight for opt in opts]

        if Game.merge_charge < Config.merge_goal:
            Game.merge_charge += 1

        if Settings.merge:
            if Game.merge_charge >= Config.merge_goal:
                opt = Method.merge
                values.insert(0, opt.value)
                weights.insert(0, opt.weight)

        value = random.choices(values, weights=weights, k=1)[0]

        if value == Method.merge.value:
            if Ants.merge():
                Game.merge_charge = 0
                return

            value = Method.sentence_4.value

        status = ""
        method = "normal"

        if value == Method.triumph.value:
            ant.triumph += 1
            method = "triumph"

        elif value == Method.hit.value:
            ant.hits += 1
            method = "hit"

        elif value == Method.travel.value:
            status = Utils.random_country([])
            method = "travel"

        elif value == Method.thinking_1.value:
            status = Utils.random_name([], Ants.get_names())
            method = "thinking"

        elif value == Method.thinking_2.value:
            status = Utils.random_emoji(3)
            method = "thinking"

        elif value == Method.sentence_1.value:
            status = Utils.rand_sentence.simple_sentence()

        elif value == Method.sentence_2.value:
            status = Utils.rand_sentence.bare_bone_sentence()

        elif value == Method.sentence_3.value:
            status = Utils.rand_sentence.bare_bone_with_adjective()

        elif value >= Method.sentence_4.value:
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
        title = Config.title
        version = Config.version
        Game.message(f"Welcome to {title} v{version}")

    @staticmethod
    def menu() -> None:
        menu = QMenu(Window.root.widget())

        style = f"""
        QMenu::separator {{
            background-color: {Config.alt_border_color};
        }}
        """

        menu.setStyleSheet(style)
        menu.setObjectName("main_menu")
        update = QAction("Update")
        restart = QAction("Restart")
        enable_all = QAction("Enable All")
        disable_all = QAction("Disable All")
        about = QAction("About")

        def make(text: str, enabled: bool) -> QAction:
            if enabled:
                icon = Config.icon_on
                word = "On"
            else:
                icon = Config.icon_off
                word = "Off"

            return QAction(f"{icon} {text} {word}")

        if Settings.merge:
            merge = make("Merge", True)
        else:
            merge = make("Merge", False)

        if Settings.score_enabled:
            score = make("Score", True)
        else:
            score = make("Score", False)

        if Settings.travel_enabled:
            travel = make("Travel", True)
        else:
            travel = make("Travel", False)

        if Settings.think_enabled:
            think = make("Think", True)
        else:
            think = make("Think", False)

        if Settings.words_enabled:
            words = make("Words", True)
        else:
            words = make("Words", False)

        update.triggered.connect(Game.force_update)
        restart.triggered.connect(Game.restart)
        merge.triggered.connect(Settings.toggle_merge)
        score.triggered.connect(Settings.toggle_score_enabled)
        travel.triggered.connect(Settings.toggle_travel_enabled)
        think.triggered.connect(Settings.toggle_think_enabled)
        words.triggered.connect(Settings.toggle_words_enabled)
        enable_all.triggered.connect(Settings.enable_all)
        disable_all.triggered.connect(Settings.disable_all)
        about.triggered.connect(Game.about)

        menu.addAction(update)
        menu.addAction(restart)
        menu.addSeparator()
        menu.addAction(merge)
        menu.addAction(score)
        menu.addAction(travel)
        menu.addAction(think)
        menu.addAction(words)
        menu.addSeparator()
        menu.addAction(enable_all)
        menu.addAction(disable_all)
        menu.addSeparator()
        menu.addAction(about)
        menu.exec_(QCursor.pos())

    @staticmethod
    def force_update() -> None:
        Game.get_status()
        Game.start_loop()

    @staticmethod
    def about() -> None:
        lines = [
            f"{Config.title} v{Config.version}    {Config.ant}",
            "Listen to the ants and watch them go.",
            "Just run it and leave it open on your screen.",
            "5% of revenue goes to the local ant shelter.",
        ]

        Window.alert("\n\n".join(lines))
