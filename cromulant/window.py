from __future__ import annotations

from PySide6.QtWidgets import QApplication  # type: ignore
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from .config import Config


class Window:
    app: QApplication
    window: QMainWindow
    root: QHBoxLayout
    view: QGraphicsView
    view_scene: QGraphicsScene
    log: QTextEdit

    @staticmethod
    def prepare() -> None:
        Window.make()
        Window.add_buttons()
        Window.add_view()
        Window.add_log()
        Window.start()

    @staticmethod
    def make() -> None:
        Window.app = QApplication([])
        Window.window = QMainWindow()
        Window.window.setWindowTitle(Config.title)
        Window.window.resize(Config.width, Config.height)
        Window.root = QHBoxLayout()
        central_widget = QWidget()
        Window.root = QVBoxLayout()
        central_widget.setLayout(Window.root)
        Window.window.setCentralWidget(central_widget)
        Window.window.setWindowIcon(QIcon(str(Config.icon_path)))
        Window.app.setStyleSheet("QWidget { background-color: #3c3681; color: #FFF; }")

    @staticmethod
    def add_buttons() -> None:
        btn_hatch = QPushButton("Hatch")
        btn_terminate = QPushButton("Terminate")
        btn_update = QPushButton("Update")
        btn_close = QPushButton("Close")

        btn_hatch.clicked.connect(Window.hatch)
        btn_terminate.clicked.connect(Window.terminate)
        btn_update.clicked.connect(Window.update_view)
        btn_close.clicked.connect(Window.close)

        layout = QHBoxLayout()
        layout.addWidget(btn_hatch)
        layout.addWidget(btn_terminate)
        layout.addWidget(btn_update)
        layout.addWidget(btn_close)

        Window.root.addLayout(layout)

    @staticmethod
    def add_view() -> None:
        Window.view = QVBoxLayout()
        Window.root.addLayout(Window.view)

    @staticmethod
    def add_log() -> None:
        container = QHBoxLayout()

        image_label = QLabel()
        pixmap = QPixmap(str(Config.image_path))
        scaled_pixmap = pixmap.scaled(100, pixmap.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setFixedWidth(100)
        container.addWidget(image_label)

        Window.log = QTextEdit()
        Window.log.setReadOnly(True)
        Window.log.setFixedHeight(100)
        container.addWidget(Window.log)

        Window.root.addLayout(container)

    @staticmethod
    def update_view() -> None:
        from .game import Game
        Game.update_view()

    @staticmethod
    def hatch() -> None:
        from .ants import Ants
        Ants.hatch()

    @staticmethod
    def terminate() -> None:
        from .ants import Ants
        Ants.terminate()

    @staticmethod
    def start() -> None:
        Window.window.show()
        Window.app.exec()

    @staticmethod
    def close() -> None:
        Window.app.quit()
