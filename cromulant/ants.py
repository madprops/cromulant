from __future__ import annotations

import random
from typing import ClassVar, Any

from .config import Config
from .utils import Utils
from .storage import Storage


class Ant:
    def __init__(self) -> None:
        now = Utils.now()
        self.created = now
        self.updated = now
        self.name = ""
        self.status = ""
        self.hits = 0
        self.triumph = 0
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
        self.color = tuple(data["color"])

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
        objs = Storage.get_ants()

        for obj in objs:
            ant = Ant()
            ant.from_dict(obj)
            Ants.ants.append(ant)

    @staticmethod
    def hatch() -> None:
        if len(Ants.ants) >= Config.max_ants:
            Utils.print("Too many ants")
            return

        now = Utils.now()

        ant = Ant()
        ant.created = now
        ant.updated = now
        ant.name = Utils.random_name()
        ant.color = Utils.random_color()

        Ants.ants.append(ant)
        Ants.save()
        Utils.print(f"Ant hatched: {ant.name}")

    @staticmethod
    def terminate() -> None:
        pass

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
    def get_other(ant: Ant) -> Ant:
        ants = [a for a in Ants.ants if a.name != ant.name]
        return random.choice(ants)
