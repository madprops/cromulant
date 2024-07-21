from __future__ import annotations

import re
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
        self.method = ""
        self.triumph = 0
        self.hits = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "created": self.created,
            "updated": self.updated,
            "name": self.name,
            "status": self.status,
            "method": self.method,
            "hits": self.hits,
            "triumph": self.triumph,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        self.created = data["created"]
        self.updated = data["updated"]
        self.name = data["name"]
        self.status = data["status"]
        self.method = data["method"]
        self.hits = data["hits"]
        self.triumph = data["triumph"]

    def get_name(self) -> str:
        return self.name or "Nameless"

    def get_age(self) -> str:
        now = Utils.now()
        return Utils.time_ago(self.created, now)

    def describe(self) -> None:
        Utils.print(f"Name is {self.get_name()}")
        Utils.print(f"It hatched {self.get_age()}")

    def get_score(self) -> int:
        return self.triumph - self.hits


class Ants:
    ants: ClassVar[list[Ant]] = []

    @staticmethod
    def prepare() -> None:
        Ants.get_ants()

    @staticmethod
    def hatch(num: int = 1) -> None:
        from .game import Game

        if len(Ants.ants) >= Config.max_ants:
            Window.alert("Max ants reached\nTerminate some to hatch new ones")
            return

        now = Utils.now()

        for _ in range(num):
            ant = Ant()
            ant.created = now
            ant.updated = now
            ant.name = Ants.random_name()

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

        if Ants.empty():
            return

        ant = Ants.random_ant()

        if not ant:
            return

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
    def random_ant(ignore: list[Ant] | None = None) -> Ant | None:
        if Ants.empty():
            return None

        if ignore:
            ants = [a for a in Ants.ants if a not in ignore]
        else:
            ants = Ants.ants

        return random.choice(ants)

    @staticmethod
    def get_names() -> list[str]:
        return [ant.name for ant in Ants.ants]

    @staticmethod
    def save() -> None:
        Storage.save_ants(Ants.ants)

    @staticmethod
    def empty() -> bool:
        return len(Ants.ants) == 0

    @staticmethod
    def get_next() -> Ant | None:
        if Ants.empty():
            return None

        now = Utils.now()
        ages = [(now - ant.updated) for ant in Ants.ants]

        # Normalize ages to create weights
        total_age = sum(ages)

        if total_age == 0:
            weights = [1] * len(Ants.ants)  # If all ages are zero, use equal weights
        else:
            weights = [
                int(age / total_age * 1000) for age in ages
            ]  # Scale and cast to int

        # Perform weighted random selection
        return random.choices(Ants.ants, weights=weights, k=1)[0]

    @staticmethod
    def get_current() -> Ant | None:
        if Ants.empty():
            return None

        return max(Ants.ants, key=lambda ant: ant.updated)

    @staticmethod
    def set_status(ant: Ant, status: str, method: str) -> None:
        from .game import Game

        status = status.strip()
        ant.status = status
        ant.method = method
        ant.updated = Utils.now()

        Game.add_status(ant)
        Ants.save()

    @staticmethod
    def get_ants() -> None:
        objs = Storage.get_ants()
        changed = False

        if len(objs) > Config.max_ants:
            objs = objs[: Config.max_ants]
            changed = True

        for obj in objs:
            ant = Ant()
            ant.from_dict(obj)
            Ants.ants.append(ant)

        if changed:
            Ants.save()

    @staticmethod
    def random_name() -> str:
        return Utils.random_name(Ants.get_names())

    @staticmethod
    def get_top_ant() -> tuple[Ant, int] | None:
        if Ants.empty():
            return None

        top = None
        top_score = 0

        # This could be a one-liner but I might expand the algorithm later
        for ant in Ants.ants:
            score = ant.get_score()

            if score <= 0:
                continue

            if (not top) or (score > top_score):
                top = ant
                top_score = score

        if not top:
            return None

        return top, top_score

    @staticmethod
    def merge() -> None:
        from .game import Game

        if len(Ants.ants) < 2:
            return

        def split(ant: Ant) -> list[str]:
            return re.split(r"[ -]", ant.name)

        def fill(words: list[str]) -> list[str]:
            if len(words) < 2:
                words.extend(Utils.random_word(2 - len(words)))

            words = [
                word if word.lower() != "of" else Utils.random_word()[0] for word in words
            ]

            words = [Utils.capitalize(word) for word in words]
            return [word.lower() if word == "de" else word for word in words]

        ant_1 = Ants.random_ant()

        if not ant_1:
            return

        ant_2 = Ants.random_ant([ant_1])

        if not ant_2:
            return

        words_1 = split(ant_1)
        words_2 = split(ant_2)

        words_1 = fill(words_1)
        words_2 = fill(words_2)

        name = ""

        for _ in range(12):
            name = f"{random.choice(words_1)} {random.choice(words_2)}"

            if (name == ant_1.name) or (name == ant_2.name):
                continue

            if name in Utils.names:
                continue

        if not name:
            return

        Ants.ants.remove(ant_1)
        Ants.ants.remove(ant_2)
        now = Utils.now()

        ant = Ant()
        ant.name = name
        ant.created = now
        ant.updated = now
        ant.triumph = ant_1.triumph + ant_2.triumph
        ant.hits = ant_1.hits + ant_2.hits

        Ants.ants.append(ant)
        Ants.save()

        image_path = Config.hatched_image_path
        Game.add_message("Merged", f"{ant.name} is born", image_path)
        Game.update_info()
