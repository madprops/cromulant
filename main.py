from __future__ import annotations

from database import Database
from window import Window
from ants import Ants


def main() -> None:
    Database.prepare()
    Database.create()

    Ants.get_all()

    for ant in Ants.ants:
        ant.describe()

    Window.make()
    Window.add_buttons()
    Window.add_view()
    Window.start()


if __name__ == "__main__":
    main()
