from __future__ import annotations

import random
from typing import Any, ClassVar

from PySide6.QtWidgets import QHBoxLayout  # type: ignore
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtGui import QCursor  # type: ignore
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QAction
from PySide6.QtCore import QPropertyAnimation  # type: ignore
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QEasingCurve
from PySide6.QtCore import QSize
from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt

from .config import Config
from .args import Args
from .utils import Utils
from .ants import Ant
from .ants import Ants
from .window import Window
from .window import RestartDialog
from .settings import Settings


class Method:
    merge = "merge"
    triumph = "triumph"
    hit = "hit"
    travel = "travel"
    think = "think"
    words = "words"


class Opt:
    value = 0

    def __init__(self, weight: int, method: str) -> None:
        self.value = Opt.value
        self.weight = weight
        self.method = method

        Opt.value += 1


class Opts:
    merge: Opt
    triumph: Opt
    hit: Opt
    travel: Opt
    think: Opt
    words: Opt

    @staticmethod
    def prepare() -> None:
        from .args import Args

        Opts.merge = Opt(Args.weight_merge, Method.merge)
        Opts.triumph = Opt(Args.weight_triumph, Method.triumph)
        Opts.hit = Opt(Args.weight_hit, Method.hit)
        Opts.travel = Opt(Args.weight_travel, Method.travel)
        Opts.think = Opt(Args.weight_think, Method.think)
        Opts.words = Opt(Args.weight_words, Method.words)

    @staticmethod
    def opts_score() -> list[Opt]:
        return [Opts.triumph, Opts.hit]

    @staticmethod
    def opts_travel() -> list[Opt]:
        return [Opts.travel]

    @staticmethod
    def opts_think() -> list[Opt]:
        return [Opts.think]

    @staticmethod
    def opts_words() -> list[Opt]:
        return [Opts.words]


class Game:
    timer: QTimer
    playing_song: bool = False
    merge_charge: int = 0
    speed: str = "paused"
    animations: ClassVar[list[QPropertyAnimation]] = []
    started: bool = False

    @staticmethod
    def prepare() -> None:
        Opts.prepare()
        Game.timer = QTimer()
        Game.timer.timeout.connect(Game.get_status)

        Game.fill()
        Game.info()

        if Args.intro:
            Game.intro()

    @staticmethod
    def update(ant: Ant) -> None:
        root = QWidget()
        container = QHBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)
        container.setContentsMargins(0, 0, 0, 0)

        if Args.images:
            image_label = Game.get_image(ant)
            container.addWidget(image_label)

        right_container = Game.make_right_container(ant)
        container.addWidget(right_container)

        container.addSpacing(Config.space_1)
        root.setLayout(container)
        Game.add_item(root)

    @staticmethod
    def message(text: str) -> None:
        root = QWidget()
        root.setContentsMargins(0, 10, 0, 10)

        container = QHBoxLayout()
        container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_line = QFrame()
        left_line.setFrameShape(QFrame.Shape.HLine)
        left_line.setFrameShadow(QFrame.Shadow.Sunken)
        left_line.setObjectName("horizontal_line")
        left_line.setFixedHeight(2)
        Window.expand_2(left_line)

        label = QLabel(text)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        right_line = QFrame()
        right_line.setFrameShape(QFrame.Shape.HLine)
        right_line.setFrameShadow(QFrame.Shadow.Sunken)
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

        animation: QPropertyAnimation | None = None

        if Game.started and Args.fade:
            animation = Game.add_fade(item)

        Window.view.insertWidget(0, item)

        if animation:
            animation.start()

        while Window.view.count() > Config.max_updates:
            layout_item = Window.view.takeAt(Window.view.count() - 1)

            if layout_item:
                if layout_item.widget():
                    layout_item.widget().deleteLater()
                elif layout_item.layout():
                    Window.delete_layout(layout_item.layout())

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
        container.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel(title)

        title_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        title_label.setStyleSheet("font-weight: bold;")
        title_label.setWordWrap(True)
        title_label.setObjectName("view_title")
        Window.expand(title_label)

        message_label = QLabel(message)

        message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

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
        elif ant == Ants.top:
            path = Config.top_image_path
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
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        image_label.setPixmap(scaled_pixmap)
        adjusted_size = scaled_pixmap.size() + QSize(4, 4)
        image_label.setFixedSize(adjusted_size)

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
            opts.extend(Opts.opts_score())

        if Settings.travel_enabled:
            opts.extend(Opts.opts_travel())

        if Settings.think_enabled:
            opts.extend(Opts.opts_think())

        if Settings.words_enabled:
            opts.extend(Opts.opts_words())

        if not opts:
            return

        values = [opt.value for opt in opts]
        weights = [opt.weight for opt in opts]

        if Game.merge_charge < Config.merge_goal:
            Game.merge_charge += 1

        if Settings.merge:
            only_merge = (len(values) == 1) and (values[0] == Opts.merge.value)

            if (Game.merge_charge >= Config.merge_goal) or only_merge:
                opt = Opts.merge
                values.insert(0, opt.value)
                weights.insert(0, opt.weight)

        value = random.choices(values, weights=weights, k=1)[0]

        if value == Opts.merge.value:
            if Ants.merge():
                Game.merge_charge = 0
                return

            value = Opts.words.value

        status = ""
        method = ""
        is_score = False

        if value == Opts.triumph.value:
            ant.triumph += 1
            method = Opts.triumph.method
            is_score = True

        elif value == Opts.hit.value:
            ant.hits += 1
            method = Opts.hit.method
            is_score = True

        elif value == Opts.travel.value:
            status = Utils.random_country([])
            method = Opts.travel.method

        elif value == Opts.think.value:
            method = Opts.think.method
            n = random.choices([1, 2, 3], weights=[1, 2, 2])[0]

            if n == 1:
                status = Utils.random_name([], Ants.get_names())
            elif n == 2:
                status = Utils.random_emoji(3)
            elif n == 3:
                status = Utils.random_word(noun=True, adj=False)

        elif value == Opts.words.value:
            method = Opts.words.method
            n = random.randint(1, 4)

            if n == 1:
                status = Utils.words_1()
            elif n == 2:
                status = Utils.words_2()
            elif n == 3:
                status = Utils.words_3()
            elif n == 4:
                status = Utils.words_4()

        else:
            status = "???"
            method = "unknown"

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
        Game.timer.stop()
        speed = Settings.speed

        if speed == "fast":
            minutes = (Args.fast_seconds or Config.fast_seconds) / 60
        elif speed == "normal":
            minutes = Args.normal_minutes or Config.normal_minutes
        elif speed == "slow":
            minutes = Args.slow_minutes or Config.slow_minutes
        else:
            Game.speed = "paused"
            return

        Game.speed = speed
        msecs = int(minutes * 60 * 1000)

        if msecs < 1000:
            msecs = 1000

        Game.timer.setInterval(msecs)
        Game.timer.start()

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
            top = Ants.top

            if top:
                score = top.get_score()
                text.append(f"Top:{nb}{top.name} ({score})")

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
        sizes = ["25", "50", "100", "250"]
        defindex = 0

        for i, opt in enumerate(sizes):
            if int(opt) == Config.default_population:
                defindex = i
                break

        size_opts = [f"{opt} ants" for opt in sizes]
        dialog = RestartDialog(size_opts, defindex)
        data: dict[str, Any] | None = None

        if dialog.exec() == QDialogButtonBox.StandardButton.Ok:
            data = dialog.get_data()

        if not data:
            return

        size = int(data["size"].split(" ")[0])

        Game.started = False
        Game.timer.stop()
        Game.merge_charge = 0
        Window.clear_view()
        Ants.populate(size)
        Window.to_top()
        Game.intro()
        Game.start_loop()
        Game.started = True

    @staticmethod
    def update_size() -> None:
        pass

    @staticmethod
    def image_action(event: QMouseEvent, ant: Ant) -> None:
        def is_terminated() -> bool:
            return ant.method == "terminated"

        if event.button() == Qt.MouseButton.LeftButton:
            if is_terminated():
                return

            Ants.terminate(ant)
            Game.start_loop()
        elif event.button() == Qt.MouseButton.MiddleButton:
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
        close = QAction("Close")

        def make(text: str, enabled: bool) -> QAction:
            if enabled:
                icon = Config.icon_on
                word = "On"
            else:
                icon = Config.icon_off
                word = "Off"

            return QAction(f"{icon} {text} {word}")

        merge = make("Merge", Settings.merge)
        score = make("Score", Settings.score_enabled)
        travel = make("Travel", Settings.travel_enabled)
        think = make("Think", Settings.think_enabled)
        words = make("Words", Settings.words_enabled)
        verbose = make("Verbose", Settings.verbose)

        update.triggered.connect(Game.force_update)
        restart.triggered.connect(Game.restart)
        merge.triggered.connect(Settings.toggle_merge)
        score.triggered.connect(Settings.toggle_score_enabled)
        travel.triggered.connect(Settings.toggle_travel_enabled)
        think.triggered.connect(Settings.toggle_think_enabled)
        words.triggered.connect(Settings.toggle_words_enabled)
        verbose.triggered.connect(Settings.toggle_verbose)
        enable_all.triggered.connect(Settings.enable_all)
        disable_all.triggered.connect(Settings.disable_all)
        about.triggered.connect(Game.about)
        close.triggered.connect(Window.close)

        menu.addAction(update)
        menu.addAction(restart)
        menu.addSeparator()
        menu.addAction(merge)
        menu.addAction(score)
        menu.addAction(travel)
        menu.addAction(think)
        menu.addAction(words)
        menu.addAction(verbose)
        menu.addSeparator()
        menu.addAction(enable_all)
        menu.addAction(disable_all)
        menu.addSeparator()
        menu.addAction(about)
        menu.addAction(close)
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
        ]

        Window.alert("\n\n".join(lines))

    @staticmethod
    def slowdown() -> None:
        if Game.speed == "slow":
            Game.change_speed("paused")
        else:
            Game.change_speed("slow")

    @staticmethod
    def change_speed(speed: str) -> None:
        Window.speed.setCurrentText(speed.capitalize())

    @staticmethod
    def filter_top() -> None:
        from .filter import Filter

        value = Filter.get_value()
        ant = Ants.top

        if not ant:
            return

        if value == ant.name.lower():
            Filter.clear()
        else:
            Filter.set_value(ant.name)

    @staticmethod
    def add_fade(item: QWidget) -> QPropertyAnimation:
        opacity = QGraphicsOpacityEffect(item)
        item.setGraphicsEffect(opacity)
        animation = QPropertyAnimation(opacity, QByteArray(b"opacity"))
        animation.setDuration(Config.fade_duration)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        def on_finish() -> None:
            item.setGraphicsEffect(None)  # pyright: ignore
            Game.animations.remove(animation)

        animation.finished.connect(on_finish)
        Game.animations.append(animation)
        return animation
