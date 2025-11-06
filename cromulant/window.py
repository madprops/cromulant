from __future__ import annotations

from typing import Any
from collections.abc import Callable
import signal

from PySide6.QtWidgets import QApplication  # type: ignore
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLayout
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QShortcut  # type: ignore
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QFontDatabase
from PySide6.QtGui import QIcon
from PySide6.QtGui import QKeyEvent
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtCore import QUrl
from PySide6.QtCore import Signal
from PySide6.QtMultimedia import QMediaPlayer  # type: ignore
from PySide6.QtMultimedia import QAudioOutput

from .config import Config
from .args import Args
from .utils import Utils


class SpecialButton(QPushButton):  # type: ignore
    middleClicked = Signal()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.MiddleButton:
            self.middleClicked.emit()
        else:
            super().mousePressEvent(e)


class SpecialComboBox(QComboBox):  # type: ignore
    middleClicked = Signal()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.MiddleButton:
            self.middleClicked.emit()
        else:
            super().mousePressEvent(e)


class FilterLineEdit(QLineEdit):  # type: ignore
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Escape:
            self.clear()
        else:
            super().keyPressEvent(e)


class RestartDialog(QDialog):  # type: ignore
    def __init__(self, sizes: list[str], defindex: int) -> None:
        super().__init__()
        self.setWindowTitle("Select Option")
        self.setFixedSize(300, 150)

        self.main_layout = QVBoxLayout()

        self.label = QLabel("Size of the population")
        self.main_layout.addWidget(self.label)

        self.size_combo = QComboBox()
        self.size_combo.addItems(sizes)
        self.size_combo.setCurrentIndex(defindex)
        self.main_layout.addWidget(self.size_combo)

        self.button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)
        self.setWindowFlags(Qt.WindowType.Popup)

    def get_data(self) -> dict[str, Any]:
        return {
            "size": str(self.size_combo.currentText()),
        }


class Window:
    app: QApplication
    window: QMainWindow
    root: QVBoxLayout
    view: QVBoxLayout
    view_scene: QGraphicsScene
    speed: QComboBox
    scroll_area: QScrollArea
    top: QPushButton
    info: QPushButton
    font: str
    emoji_font: str
    mono_font: str
    player: QMediaPlayer
    audio: QAudioOutput
    filter: QLineEdit

    @staticmethod
    def prepare() -> None:
        Window.make()
        Window.add_buttons()
        Window.add_view()
        Window.add_footer()
        Window.setup_keyboard()

    @staticmethod
    def make() -> None:
        Window.app = QApplication([])
        program = Args.program or Config.program
        Window.app.setApplicationName(program)

        Window.window = QMainWindow()
        title = Args.title or Config.title
        Window.window.setWindowTitle(title)
        width = Args.width or Config.width
        height = Args.height or Config.height
        Window.window.resize(width, height)

        if Args.maximize:
            Window.window.showMaximized()

        central_widget = QWidget()
        Window.root = QVBoxLayout()
        central_widget.setLayout(Window.root)
        Window.root.setAlignment(Qt.AlignmentFlag.AlignTop)
        Window.window.setCentralWidget(central_widget)
        Window.window.setWindowIcon(QIcon(str(Config.icon_path)))
        Window.root.setContentsMargins(0, 0, 0, 0)
        Window.set_style()

    @staticmethod
    def set_style() -> None:
        font_id = QFontDatabase.addApplicationFont(str(Config.font_path))
        emoji_font_id = QFontDatabase.addApplicationFont(str(Config.emoji_font_path))
        mono_font_id = QFontDatabase.addApplicationFont(str(Config.mono_font_path))

        if font_id != -1:
            Window.font = QFontDatabase.applicationFontFamilies(font_id)[0]

        if emoji_font_id != -1:
            Window.emoji_font = QFontDatabase.applicationFontFamilies(emoji_font_id)[0]

        if mono_font_id != -1:
            Window.mono_font = QFontDatabase.applicationFontFamilies(mono_font_id)[0]

        style = f"""

        QWidget {{
            background-color: {Config.background_color};
            color: {Config.text_color};
            font-size: {Config.font_size}px;
        }}

        QMenu {{
            background-color: {Config.alt_background_color};
            color: {Config.alt_text_color};
            border: 2px solid {Config.alt_border_color};
        }}

        QMenu::item:selected {{
            background-color: {Config.alt_hover_background_color};
            color: {Config.alt_hover_text_color};
        }}

        QDialog {{
            background-color: {Config.alt_background_color};
            color: {Config.alt_text_color};
            border: 2px solid {Config.alt_border_color};
        }}

        QDialog QLabel {{
            background-color: {Config.alt_background_color};
            color: {Config.alt_text_color};
        }}

        QDialog QPushButton {{
            background-color: {Config.alt_background_color};
            color: {Config.alt_text_color};
        }}

        QDialog QPushButton:hover {{
            background-color: {Config.message_box_button_hover_background_color};
            color: {Config.message_box_button_hover_text_color};
        }}

        QComboBox {{
            selection-background-color: {Config.alt_hover_background_color};
            selection-color: {Config.alt_hover_text_color};
        }}

        QComboBox QAbstractItemView {{
            background-color: {Config.alt_background_color};
            color: {Config.alt_text_color};
            border: 2px solid {Config.alt_border_color};
            padding: 6px;
        }}

        QScrollBar:vertical {{
            border: 0px solid transparent;
            background: {Config.background_color};
            width: 15px;
            margin: 0px 0px 0px 0px;
        }}

        QScrollBar::handle:vertical {{
            background: {Config.scrollbar_handle_color};
            min-height: 20px;
        }}

        QScrollBar::add-line:vertical {{
            border: none;
            background: none;
        }}

        QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}

        QLineEdit {{
            background-color: {Config.input_background_color};
            color: {Config.input_text_color};
            border: 1px solid {Config.input_border_color};
        }}

        QFrame#horizontal_line {{
            background-color: white;
            color: white;
        }}

        QLabel#menu_label:hover {{
            background-color: {Config.alt_hover_background_color};
        }}

        """.strip()

        Window.app.setStyleSheet(style)

        if Args.mono:
            Window.app.setFont(Window.mono_font)
        else:
            Window.app.setFont(Window.font)

    @staticmethod
    def add_buttons() -> None:
        from .game import Game
        from .filter import Filter

        root = QWidget()
        container = QHBoxLayout()

        btn_menu = SpecialButton("Menu")
        btn_menu.setToolTip("The main menu\nMiddle Click: Update")
        btn_menu.clicked.connect(Game.menu)
        btn_menu.middleClicked.connect(Game.force_update)

        Window.speed = SpecialComboBox()
        tooltip = "The speed of the updates\n"

        fast = (Args.fast_seconds or Config.fast_seconds) / 60
        tooltip += f"Fast: {Utils.get_timeword(fast)}\n"

        normal = Args.normal_minutes or Config.normal_minutes
        tooltip += f"Normal: {Utils.get_timeword(normal)}\n"

        slow = Args.slow_minutes or Config.slow_minutes
        tooltip += f"Slow: {Utils.get_timeword(slow)}\n"

        tooltip += "Middle Click: Slow"
        Window.speed.setToolTip(tooltip)
        Window.speed.addItems(["Fast", "Normal", "Slow", "Paused"])
        Window.speed.setCurrentIndex(1)
        Window.speed.currentIndexChanged.connect(Game.update_speed)
        Window.speed.middleClicked.connect(Game.slowdown)
        Window.top = SpecialButton("Top")

        Window.top.setToolTip("Scroll To Top")

        Window.top.clicked.connect(Window.to_top)
        Window.filter = FilterLineEdit()
        Window.filter.setPlaceholderText("Filter")
        Window.filter.keyReleaseEvent = lambda e: Filter.filter(e)

        container.addWidget(btn_menu, 1)
        container.addWidget(Window.speed, 1)
        container.addWidget(Window.top, 1)
        container.addWidget(Window.filter, 1)

        root.setLayout(container)

        if not Args.header:
            root.setVisible(False)

        Window.root.addWidget(root)

    @staticmethod
    def add_view() -> None:
        Window.scroll_area = QScrollArea()
        Window.scroll_area.setWidgetResizable(True)

        container = QWidget()
        parent = QVBoxLayout(container)
        Window.view = QVBoxLayout()
        parent.addLayout(Window.view)

        Window.view.setAlignment(Qt.AlignmentFlag.AlignTop)
        Window.scroll_area.setWidget(container)
        Window.root.addWidget(Window.scroll_area)

    @staticmethod
    def start() -> None:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Window.window.show()
        Window.app.exec()

    @staticmethod
    def close() -> None:
        Window.app.quit()

    @staticmethod
    def delete_layout(layout: QLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()
            elif item.layout():
                Window.delete_layout(item.layout())

        layout.deleteLater()

    @staticmethod
    def expand(widget: QWidget) -> None:
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    @staticmethod
    def expand_2(widget: QWidget) -> None:
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    @staticmethod
    def clear_view() -> None:
        while Window.view.count():
            item = Window.view.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()
            elif item.layout():
                Window.delete_layout(item.layout())

    @staticmethod
    def to_top() -> None:
        Window.scroll_area.verticalScrollBar().setValue(0)

    @staticmethod
    def to_bottom() -> None:
        Window.scroll_area.verticalScrollBar().setValue(
            Window.scroll_area.verticalScrollBar().maximum()
        )

    @staticmethod
    def toggle_scroll() -> None:
        maxim = Window.scroll_area.verticalScrollBar().maximum()

        if Window.scroll_area.verticalScrollBar().value() == maxim:
            Window.to_top()
        else:
            Window.to_bottom()

    @staticmethod
    def add_footer() -> None:
        from .game import Game

        root = QWidget()
        root.setContentsMargins(0, 0, 0, 0)
        container = QHBoxLayout()
        Window.info = SpecialButton("---")

        Window.info.setToolTip(
            "Click to scroll to the bottom or top\nMiddle Click: Filter Top"
        )

        Window.info.clicked.connect(Window.toggle_scroll)
        Window.info.middleClicked.connect(Game.filter_top)
        Window.info.setMinimumSize(35, 35)
        container.addWidget(Window.info)
        root.setLayout(container)

        if not Args.footer:
            root.setVisible(False)

        Window.root.addWidget(root)

    @staticmethod
    def play_audio(path: str, on_stop: Callable[..., Any] | None = None) -> None:
        Window.player = QMediaPlayer()
        Window.audio = QAudioOutput()
        Window.player.setAudioOutput(Window.audio)
        Window.player.setSource(QUrl.fromLocalFile(path))
        Window.audio.setVolume(100)

        def handle_state_change(state: int) -> None:
            if state == QMediaPlayer.PlaybackState.StoppedState:
                if on_stop:
                    on_stop()

        Window.player.playbackStateChanged.connect(handle_state_change)
        Window.player.play()

    @staticmethod
    def stop_audio() -> None:
        Window.player.stop()

    @staticmethod
    def alert(message: str) -> None:
        msg_box = QMessageBox()
        msg_box.setWindowFlags(Qt.WindowType.Popup)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Information")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    @staticmethod
    def setup_keyboard() -> None:
        on_enter = QShortcut(QKeySequence(Qt.Key.Key_Return), Window.window)
        on_enter.activated.connect(Window.toggle_scroll)
