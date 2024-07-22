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
from PySide6.QtGui import QFontDatabase  # type: ignore
from PySide6.QtGui import QIcon
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer  # type: ignore
from PySide6.QtMultimedia import QAudioOutput

from .config import Config
from .utils import Utils


class FilterLineEdit(QLineEdit):  # type: ignore
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Escape:
            self.clear()
        else:
            super().keyPressEvent(e)


class ComboBoxDialog(QDialog):  # type: ignore
    def __init__(self, message: str, options: list[str], defindex: int) -> None:
        super().__init__()
        self.setWindowTitle("Select Option")
        self.setFixedSize(300, 150)  # Set a fixed size for the dialog

        self.layout = QVBoxLayout()

        self.label = QLabel(message)
        self.layout.addWidget(self.label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(options)
        self.combo_box.setCurrentIndex(defindex)
        self.layout.addWidget(self.combo_box)

        self.button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.button_layout.addWidget(self.ok_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def get_selection(self) -> str:
        return str(self.combo_box.currentText())


class Window:
    app: QApplication
    window: QMainWindow
    root: QVBoxLayout
    view: QVBoxLayout
    view_scene: QGraphicsScene
    speed: QComboBox
    scroll_area: QScrollArea
    info: QPushButton
    font: str
    emoji_font: str
    player: QMediaPlayer
    audio: QAudioOutput
    filter: QLineEdit

    @staticmethod
    def prepare() -> None:
        Window.make()
        Window.add_buttons()
        Window.add_view()
        Window.add_footer()

    @staticmethod
    def make() -> None:
        Window.app = QApplication([])
        Window.app.setApplicationName(Config.program)

        Window.window = QMainWindow()
        Window.window.setWindowTitle(Config.title)
        Window.window.resize(Config.width, Config.height)

        central_widget = QWidget()
        Window.root = QVBoxLayout()
        central_widget.setLayout(Window.root)
        Window.root.setAlignment(Qt.AlignTop)
        Window.window.setCentralWidget(central_widget)
        Window.window.setWindowIcon(QIcon(str(Config.icon_path)))
        Window.root.setContentsMargins(0, 0, 0, 0)
        Window.set_style()

    @staticmethod
    def set_style() -> None:
        font_id = QFontDatabase.addApplicationFont(str(Config.font_path))
        emoji_font_id = QFontDatabase.addApplicationFont(str(Config.emoji_font_path))

        if font_id != -1:
            Window.font = QFontDatabase.applicationFontFamilies(font_id)[0]

        if emoji_font_id != -1:
            Window.emoji_font = QFontDatabase.applicationFontFamilies(emoji_font_id)[0]

        style = f"""

        QWidget {{
            background-color: {Config.background_color};
            color: {Config.text_color};
            font-size: {Config.font_size}px;
        }}

        QMenu {{
            background-color: {Config.alt_background_color};
            color: {Config.alt_text_color};
            border: 1px solid {Config.alt_border_color};
        }}

        QMenu::item:selected {{
            background-color: {Config.alt_hover_background_color};
            color: {Config.alt_hover_text_color};
        }}

        QDialog {{
            background-color: {Config.alt_background_color};
            color: {Config.alt_text_color};
            border: 1px solid {Config.alt_border_color};
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
            border: 1px solid {Config.alt_border_color};
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

        """.strip()

        Window.app.setStyleSheet(style)
        Window.app.setFont(Window.font)

    @staticmethod
    def add_buttons() -> None:
        from .game import Game
        from .filter import Filter

        root = QWidget()
        container = QHBoxLayout()

        btn_restart = QPushButton("Restart")
        btn_restart.setToolTip("Restart with a new set of ants")
        btn_restart.clicked.connect(Game.restart)

        Window.speed = QComboBox()
        tooltip = "The speed of the updates\n"
        tooltip += f"Fast: {Utils.get_seconds(Config.loop_delay_fast)}\n"
        tooltip += f"Normal: {Utils.get_seconds(Config.loop_delay_normal)}\n"
        tooltip += f"Slow: {Utils.get_seconds(Config.loop_delay_slow)}"
        Window.speed.setToolTip(tooltip)
        Window.speed.addItems(["Fast", "Normal", "Slow", "Paused"])
        Window.speed.setCurrentIndex(1)
        Window.speed.currentIndexChanged.connect(Game.update_speed)

        Window.filter = FilterLineEdit()
        Window.filter.setFixedWidth(Config.filter_width)
        Window.filter.setPlaceholderText("Filter")
        Window.filter.mousePressEvent = lambda e: Window.to_top()
        Window.filter.keyReleaseEvent = lambda e: Filter.filter(e)

        container.addWidget(btn_restart)
        container.addWidget(Window.speed)
        container.addWidget(Window.filter)

        root.setLayout(container)
        Window.root.addWidget(root)

    @staticmethod
    def add_view() -> None:
        Window.scroll_area = QScrollArea()
        Window.scroll_area.setWidgetResizable(True)

        container = QWidget()
        parent = QVBoxLayout(container)
        Window.view = QVBoxLayout()
        parent.addLayout(Window.view)

        Window.view.setAlignment(Qt.AlignTop)
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
            if item.widget():
                item.widget().deleteLater()
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
            if item.widget():
                item.widget().deleteLater()
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
        root = QWidget()
        root.setContentsMargins(0, 0, 0, 0)
        container = QHBoxLayout()
        Window.info = QPushButton("---")
        Window.info.setToolTip("Click to scroll to the bottom or top")
        Window.info.clicked.connect(Window.toggle_scroll)
        Window.info.setMinimumSize(35, 35)
        container.addWidget(Window.info)
        root.setLayout(container)
        Window.root.addWidget(root)

    @staticmethod
    def play_audio(path: str, on_stop: Callable[..., Any] | None = None) -> None:
        Window.player = QMediaPlayer()
        Window.audio = QAudioOutput()
        Window.player.setAudioOutput(Window.audio)
        Window.player.setSource(QUrl.fromLocalFile(path))
        Window.audio.setVolume(100)

        def handle_state_change(state: QMediaPlayer.State) -> None:
            if state == QMediaPlayer.StoppedState:
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
        msg_box.setWindowFlags(Qt.Popup)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Information")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    @staticmethod
    def prompt_combobox(message: str, options: list[str], defindex: int = 0) -> str:
        dialog = ComboBoxDialog(message, options, defindex)
        dialog.setWindowFlags(Qt.Popup)

        if dialog.exec() == QDialog.Accepted:
            return dialog.get_selection()

        return ""
