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

from .config import Config


class Window:
    app: QApplication
    window: QMainWindow
    root: QHBoxLayout
    view: QGraphicsView
    log: QTextEdit

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

    @staticmethod
    def add_buttons() -> None:
        btn_hatch = QPushButton("Hatch")
        btn_terminate = QPushButton("Terminate")
        btn_update = QPushButton("Update")

        btn_hatch.clicked.connect(Window.hatch)
        btn_terminate.clicked.connect(Window.terminate)
        btn_update.clicked.connect(Window.update_view)

        layout = QHBoxLayout()
        layout.addWidget(btn_hatch)
        layout.addWidget(btn_terminate)
        layout.addWidget(btn_update)

        Window.root.addLayout(layout)

    @staticmethod
    def add_view() -> None:
        Window.view = QGraphicsView()
        scene = QGraphicsScene()
        Window.view.setScene(scene)
        Window.root.addWidget(Window.view)

    @staticmethod
    def add_log() -> None:
        Window.log = QTextEdit()
        Window.log.setReadOnly(True)
        Window.log.setFixedHeight(100)
        Window.root.addWidget(Window.log)

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
