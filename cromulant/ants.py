from __future__ import annotations

import random
from typing import ClassVar, Any

from .config import Config
from .utils import Utils
from .storage import Storage

from .window import Window


class Ant:
    def __init__(self) -> None:
        now = Utils.now()
        self.created = now
        self.updated = now
        self.name = ""
        self.status = ""
        self.triumph = 0
        self.hits = 0
        self.color: tuple[int, int, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "created": self.created,
            "updated": self.updated,
            "name": self.name,
            "status": self.status,
            "hits": self.hits,
            "triumph": self.triumph,
            "color": self.color,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        self.created = data["created"]
        self.updated = data["updated"]
        self.name = data["name"]
        self.status = data["status"]
        self.hits = data["hits"]
        self.triumph = data["triumph"]

        c = data["color"]
        self.color = (c[0], c[1], c[2])

    def get_name(self) -> str:
        return self.name or "Nameless"

    def get_age(self) -> str:
        now = Utils.now()
        return Utils.time_ago(self.created, now)

    def describe(self) -> None:
        Utils.print(f"Name is {self.get_name()}")
        Utils.print(f"It hatched {self.get_age()}")


class Ants:
    ants: ClassVar[list[Ant]] = []

    @staticmethod
    def prepare() -> None:
        Ants.get_ants()

    @staticmethod
    def hatch(num: int = 1) -> None:
        from .game import Game

        if len(Ants.ants) >= Config.max_ants:
            return

        now = Utils.now()

        for _ in range(num):
            ant = Ant()
            ant.created = now
            ant.updated = now
            ant.name = Utils.random_name()
            ant.color = Utils.random_color(ant.name)

            Ants.ants.append(ant)
            image_path = Config.hatched_image_path
            Game.add_message("Hatched", f"{ant.name} is born", image_path)

            if len(Ants.ants) >= Config.max_ants:
                break

        Ants.save()
        Game.update_info()

    @staticmethod
    def hatch_burst() -> None:
        Ants.hatch(Config.hatch_burst)

    @staticmethod
    def terminate() -> None:
        from .game import Game

        if not len(Ants.ants):
            return

        ant = Ants.get_random_ant()
        Ants.ants.remove(ant)
        Ants.save()

        image_path = Config.terminated_image_path
        Game.add_message("Terminated", f"{ant.name} is gone", image_path)
        Game.update_info()

    @staticmethod
    def terminate_all() -> None:
        from .game import Game

        def action() -> None:
            Ants.ants = []
            Ants.save()
            Window.clear_view()
            Game.update_info()

        Window.confirm("Terminate all ants?", action)

    @staticmethod
    def get_random_ant() -> Ant:
        return random.choice(Ants.ants)

    @staticmethod
    def get_names() -> list[str]:
        return [ant.name for ant in Ants.ants]

    @staticmethod
    def save() -> None:
        Storage.save_ants(Ants.ants)

    @staticmethod
    def get_lazy() -> Ant:
        return min(Ants.ants, key=lambda ant: ant.updated)

    @staticmethod
    def set_status(ant: Ant, status: str) -> None:
        from .game import Game

        status = status.strip()

        if not status:
            return

        ant.status = status
        ant.updated = Utils.now()
        Game.add_status(ant)
        Ants.save()

    @staticmethod
    def get_other(ant: Ant) -> Ant:
        ants = [a for a in Ants.ants if a.name != ant.name]
        return random.choice(ants)

    @staticmethod
    def get_ants() -> None:
        objs = Storage.get_ants()

        for obj in objs:
            ant = Ant()
            ant.from_dict(obj)
            Ants.ants.append(ant)

    @staticmethod
    def most_hits() -> Ant | None:
        if not len(Ants.ants):
            return None

        return max(Ants.ants, key=lambda a: a.hits)

    @staticmethod
    def most_triumph() -> Ant | None:
        if not len(Ants.ants):
            return None

        return max(Ants.ants, key=lambda a: a.triumph)
