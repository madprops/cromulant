from __future__ import annotations

from PySide6.QtWidgets import QWidget  # type: ignore
from PySide6.QtGui import QKeyEvent  # type: ignore
from PySide6.QtCore import QTimer  # type: ignore

from .config import Config
from .window import Window


class Filter:
    debouncer: QTimer

    @staticmethod
    def prepare() -> None:
        Filter.debouncer = QTimer()
        Filter.debouncer.setSingleShot(True)
        Filter.debouncer.setInterval(Config.filter_debouncer_delay)
        Filter.debouncer.timeout.connect(Filter.do_filter)

    @staticmethod
    def get_value() -> str:
        return str(Window.filter.text()).lower().strip()

    @staticmethod
    def set_value(value: str) -> None:
        Window.filter.setText(value)
        Filter.do_filter()

    @staticmethod
    def clear() -> None:
        Window.filter.clear()
        Filter.do_filter()

    @staticmethod
    def filter(event: QKeyEvent | None = None) -> None:
        Filter.debouncer.stop()
        Filter.debouncer.start()

    @staticmethod
    def do_filter() -> None:
        Filter.debouncer.stop()
        value = Filter.get_value()

        for i in range(Window.view.count()):
            item = Window.view.itemAt(i)
            text = Filter.get_text(item)
            hide = True

            for txt in text:
                if value in txt:
                    hide = False
                    break

            if hide:
                item.widget().hide()
            else:
                item.widget().show()

    @staticmethod
    def get_text(item: QWidget) -> list[str]:
        text = []
        layout = item.widget().layout()

        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()

            if not widget:
                continue

            name = widget.objectName()

            if name != "view_right":
                continue

            layout2 = widget.layout()

            for j in range(layout2.count()):
                wid = layout2.itemAt(j).widget()

                if not wid:
                    continue

                name = wid.objectName()

                if not name:
                    continue

                if (name == "view_title") or (name == "view_message"):
                    text.append(wid.text().lower())

        return text

    @staticmethod
    def check() -> None:
        value = Filter.get_value()

        if value:
            Filter.filter()
