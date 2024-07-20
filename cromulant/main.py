from __future__ import annotations

from .config import Config
from .utils import Utils
from .ants import Ants
from .window import Window
from .game import Game
from .settings import Settings


def main() -> None:
    Config.prepare()
    Utils.prepare()
    Ants.prepare()
    Window.prepare()
    Settings.prepare()
    Game.prepare()
    Game.start_loop()
    Window.start()


if __name__ == "__main__":
    main()
