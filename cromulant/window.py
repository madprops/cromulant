from __future__ import annotations

from typing import Any
from collections.abc import Callable

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
from PySide6.QtGui import QMouseEvent  # type: ignore
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt  # type: ignore
from PySide6.QtCore import Signal

from .config import Config


class SpecialButton(QPushButton):  # type: ignore
    middleClicked = Signal()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.MiddleButton:
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
        Window.root.setAlignment(Qt.AlignmentFlag.AlignTop)
        Window.window.setCentralWidget(central_widget)
        Window.window.setWindowIcon(QIcon(str(Config.icon_path)))

        style = f"QWidget {{ background-color: {Config.background_color}; \
        color: {Config.text_color}; font-size: {Config.font_size}px}}"

        Window.root.setContentsMargins(0, 0, 0, 0)
        Window.app.setStyleSheet(style)

    @staticmethod
    def add_buttons() -> None:
        from .ants import Ants
        from .game import Game

        root = QWidget()
        container = QHBoxLayout()

        btn_hatch = SpecialButton("Hatch")
        btn_hatch.clicked.connect(lambda e: Ants.hatch())
        btn_hatch.middleClicked.connect(lambda: Ants.hatch_burst())

        btn_terminate = SpecialButton("Terminate")
        btn_terminate.clicked.connect(lambda e: Ants.terminate())
        btn_terminate.middleClicked.connect(lambda: Ants.terminate_all())

        Window.speed = QComboBox()
        Window.speed.addItems(["Fast", "Normal", "Slow"])
        Window.speed.setCurrentIndex(1)
        Window.speed.currentIndexChanged.connect(Game.update_speed)

        btn_top = SpecialButton("Top")
        btn_top.clicked.connect(Window.to_top)

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

        Window.view.setAlignment(Qt.AlignmentFlag.AlignTop)
        Window.scroll_area.setWidget(container)
        Window.root.addWidget(Window.scroll_area)

    @staticmethod
    def start() -> None:
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
        Window.info.clicked.connect(Window.to_bottom)
        Window.expand(Window.info)
        container.addWidget(Window.info)
        root.setLayout(container)
        Window.root.addWidget(root)
