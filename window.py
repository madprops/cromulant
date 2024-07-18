from __future__ import annotations

from PySide6.QtWidgets import QApplication  # type: ignore
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QHBoxLayout

from config import Config
from ants import Ants


class Window:
    app: QApplication
    window: QMainWindow
    root: QWidget
    view: QGraphicsView

    @staticmethod
    def make() -> None:
        Window.app = QApplication([])
        Window.window = QMainWindow()
        Window.window.setWindowTitle(Config.title)
        Window.window.resize(Config.width, Config.height)
        Window.root = QWidget()
        Window.window.setCentralWidget(Window.root)

    @staticmethod
    def add_buttons() -> None:
        btn_hatch = QPushButton("Hatch Ant")
        btn_terminate = QPushButton("Terminate")

        btn_hatch.clicked.connect(Window.hatch)
        btn_terminate.clicked.connect(Window.terminate)

        layout = QHBoxLayout()
        layout.addWidget(btn_hatch)
        layout.addWidget(btn_terminate)

        Window.root.setLayout(layout)

    @staticmethod
    def add_view() -> None:
        Window.view = QGraphicsView()
        scene = QGraphicsScene()
        Window.view.setScene(scene)
        layout = QVBoxLayout(Window.root)
        layout.addWidget(Window.view)

    @staticmethod
    def hatch() -> None:
        Ants.hatch()

    @staticmethod
    def terminate() -> None:
        Ants.terminate()

    @staticmethod
    def start() -> None:
        Window.window.show()
        Window.app.exec()
