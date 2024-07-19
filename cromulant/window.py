from __future__ import annotations

from PySide6.QtWidgets import QApplication  # type: ignore
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QLayout
from PySide6.QtGui import QIcon  # type: ignore
from PySide6.QtCore import Qt  # type: ignore

from .config import Config


class Window:
    app: QApplication
    window: QMainWindow
    root: QVBoxLayout
    view: QVBoxLayout
    view_scene: QGraphicsScene

    @staticmethod
    def prepare() -> None:
        Window.make()
        Window.add_buttons()
        Window.add_view()

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
        color: {Config.text_color}; font-size: 20px}}"

        Window.app.setStyleSheet(style)

    @staticmethod
    def add_buttons() -> None:
        btn_hatch = QPushButton("Hatch")
        btn_terminate = QPushButton("Terminate")
        btn_close = QPushButton("Close")

        btn_hatch.clicked.connect(Window.hatch)
        btn_terminate.clicked.connect(Window.terminate)
        btn_close.clicked.connect(Window.close)

        layout = QHBoxLayout()
        layout.addWidget(btn_hatch)
        layout.addWidget(btn_terminate)
        layout.addWidget(btn_close)

        Window.root.addLayout(layout)

    @staticmethod
    def add_view() -> None:
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        parent = QVBoxLayout(container)
        Window.view = QVBoxLayout()
        parent.addLayout(Window.view)

        Window.view.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(container)
        Window.root.addWidget(scroll_area)

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

    @staticmethod
    def delete_layout(layout: QLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                Window.delete_layout(item.layout())

        layout.deleteLater()
