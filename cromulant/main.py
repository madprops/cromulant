from __future__ import annotations

from .config import Config
from .database import Database
from .window import Window
from .ants import Ants


def main() -> None:
    Config.prepare()
    Database.prepare()
    Database.create()

    Ants.get_all()

    Window.make()
    Window.add_buttons()
    Window.add_view()
    Window.add_log()
    Window.start()


if __name__ == "__main__":
    main()
