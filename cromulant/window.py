from __future__ import annotations

from typing import Any
from collections.abc import Callable
import signal

from PySide6.QtWidgets import QApplication  # type: ignore
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLayout
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QFontDatabase  # type: ignore
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtCore import Signal
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer  # type: ignore
from PySide6.QtMultimedia import QAudioOutput

from .config import Config


class SpecialButton(QPushButton):  # type: ignore
    middleClicked = Signal()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MiddleButton:
            self.middleClicked.emit()
        else:
            super().mousePressEvent(e)


class Window:
    app: QApplication
    window: QMainWindow
    root: QVBoxLayout
    view: QVBoxLayout
    view_scene: QGraphicsScene
    speed: QComboBox
    scroll_area: QScrollArea
    info: SpecialButton
    font: str
    emoji_font: str
    player: QMediaPlayer
    audio: QAudioOutput

    @staticmethod
    def prepare() -> None:
        Window.make()
        Window.add_buttons()
        Window.add_view()
        Window.add_footer()

    @staticmethod
    def make() -> None:
        Window.app = QApplication([])
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
            background-color: {Config.context_menu_background_color};
            color: {Config.context_menu_text_color};
        }}

        QMenu::item:selected {{
            background-color: {Config.context_menu_hover_background_color};
            color: {Config.context_menu_hover_text_color};
        }}

        QMessageBox {{
            background-color: {Config.message_box_background_color};
            color: {Config.message_box_text_color};
        }}

        QMessageBox QLabel {{
            background-color: {Config.message_box_background_color};
            color: {Config.message_box_label_text_color};
        }}

        QMessageBox QPushButton {{
            background-color: {Config.message_box_button_background_color};
            color: {Config.message_box_button_text_color};
        }}

        QMessageBox QPushButton:hover {{
            background-color: {Config.message_box_button_hover_background_color};
            color: {Config.message_box_button_hover_text_color};
        }}
        """.strip()

        Window.app.setStyleSheet(style)
        Window.app.setFont(Window.font)

    @staticmethod
    def add_buttons() -> None:
        from .ants import Ants
        from .game import Game

        root = QWidget()
        container = QHBoxLayout()

        btn_hatch = SpecialButton("Hatch")
        btn_hatch.setToolTip("Hatch a new ant\nMiddle Click to hatch Trio")
        btn_hatch.clicked.connect(lambda e: Ants.hatch())
        btn_hatch.middleClicked.connect(lambda: Ants.hatch_burst())

        btn_terminate = SpecialButton("Terminate")

        btn_terminate.setToolTip(
            "Terminate a random ant\nMiddle Click to terminate all"
        )

        btn_terminate.clicked.connect(lambda e: Ants.terminate())
        btn_terminate.middleClicked.connect(lambda: Ants.terminate_all())

        Window.speed = QComboBox()
        Window.speed.setToolTip("Change the speed of the updates")
        Window.speed.addItems(["Fast", "Normal", "Slow"])
        Window.speed.setCurrentIndex(1)
        Window.speed.currentIndexChanged.connect(Game.update_speed)

        btn_top = SpecialButton("Top")
        btn_top.setToolTip("Scroll to the top\nMiddle Click to scroll to the bottom")
        btn_top.clicked.connect(Window.to_top)
        btn_top.middleClicked.connect(Window.to_bottom)

        container.addWidget(btn_hatch)
        container.addWidget(btn_terminate)
        container.addWidget(Window.speed)
        container.addWidget(btn_top)

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
    def confirm(message: str, action: Callable[..., Any]) -> None:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Confirm")
        msg_box.setText(message)

        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.button(QMessageBox.StandardButton.Yes).clicked.connect(action)
        msg_box.exec()

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
    def add_footer() -> None:
        root = QWidget()
        root.setContentsMargins(0, 0, 0, 0)
        container = QHBoxLayout()
        Window.info = SpecialButton("---")
        Window.info.setToolTip(
            "Scroll to the bottom\nMiddle Click to scroll to the top"
        )
        Window.info.clicked.connect(Window.to_bottom)
        Window.info.middleClicked.connect(Window.to_top)
        Window.info.setMinimumSize(35, 35)
        container.addWidget(Window.info)
        root.setLayout(container)
        Window.root.addWidget(root)

    @staticmethod
    def play_audio(path: str) -> None:
        Window.player = QMediaPlayer()
        Window.audio = QAudioOutput()
        Window.player.setAudioOutput(Window.audio)
        Window.player.setSource(QUrl.fromLocalFile(path))
        Window.audio.setVolume(100)
        Window.player.play()

    @staticmethod
    def stop_audio() -> None:
        Window.player.stop()

    @staticmethod
    def alert(message: str) -> None:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Information")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()