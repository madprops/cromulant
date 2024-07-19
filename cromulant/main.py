from __future__ import annotations

from .config import Config
from .utils import Utils
from .ants import Ants
from .window import Window


def main() -> None:
    Config.prepare()
    Utils.prepare()
    Ants.prepare()
    Window.prepare()


if __name__ == "__main__":
    main()
