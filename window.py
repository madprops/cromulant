from __future__ import annotations

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QVBoxLayout

from ants import Ants


class Window:
    title = "Cromulant"
    width = 800
    height = 600
    app: QApplication
    window: QMainWindow
    root: QWidget

    @staticmethod
    def make() -> None:
        Window.app = QApplication([])
        Window.window = QMainWindow()
        Window.window.setWindowTitle(Window.title)
        Window.window.resize(Window.width, Window.height)
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
        Window.scene = QGraphicsScene()
        Window.view.setScene(Window.scene)

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
