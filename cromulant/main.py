from __future__ import annotations

from .config import Config
from .utils import Utils
from .ants import Ants
from .window import Window
from .game import Game
from .settings import Settings
from .filter import Filter


def main() -> None:
    Config.prepare()
    Utils.prepare()
    Window.prepare()
    Ants.prepare()
    Settings.prepare()
    Filter.prepare()
    Game.prepare()
    Game.start_loop()
    Window.start()


if __name__ == "__main__":
    main()
