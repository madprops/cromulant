from __future__ import annotations

import os
import sys
import fcntl
import tempfile
from pathlib import Path

from .config import Config
from .utils import Utils
from .ants import Ants
from .window import Window
from .game import Game
from .settings import Settings
from .filter import Filter
from .args import Args


def main() -> None:
    Config.prepare()
    Args.prepare()

    if Args.argdoc:
        Args.make_argdoc()
        sys.exit(0)

    program = Config.program
    title = Config.title

    pid = f"{program}.pid"
    pid_file = Path(tempfile.gettempdir(), pid)
    fp = pid_file.open("w", encoding="utf-8")

    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        Utils.print(f"{title} is already running.")
        sys.exit(0)

    # Create singleton
    fp.write(str(os.getpid()))
    fp.flush()

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
