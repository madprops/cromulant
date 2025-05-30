from __future__ import annotations

import re
import random
import itertools
from typing import ClassVar, Any

from .config import Config
from .args import Args
from .utils import Utils
from .storage import Storage
from .settings import Settings


class Ant:
    def __init__(self) -> None:
        now = Utils.now()
        self.created = now
        self.updated = now
        self.name = ""
        self.status = ""
        self.method = "hatched"
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

    def tooltip(self) -> str:
        tooltip = ""
        tooltip += f"Updated: {Utils.to_date(self.updated)}"
        tooltip += f"\nCreated: {Utils.to_date(self.created)}"
        tooltip += f"\nTriumph: {self.triumph} | Hits: {self.hits}"
        tooltip += "\nClick to Terminate"
        tooltip += "\nMiddle Click to Merge"
        return tooltip

    def get_status(self) -> str:
        from .game import Method

        if (not self.status) and (not self.method):
            return "No update yet"

        status = self.status

        if self.method == Method.triumph:
            if Args.score:
                total = f"(Score: {self.get_score()})"
            else:
                total = f"({self.triumph} total)"

            status = f"{Config.triumph_icon} {Config.triumph_message} {total}"

        elif self.method == Method.hit:
            if Args.score:
                total = f"(Score: {self.get_score()})"
            else:
                total = f"({self.hits} total)"

            status = f"{Config.hit_icon} {Config.hit_message} {total}"

        elif self.method == Method.think:
            status = f"Thinking about {status}"

        elif self.method == Method.travel:
            status = f"Traveling to {status}"

        return status


class Ants:
    ants: ClassVar[list[Ant]] = []
    top: ClassVar[Ant | None] = None

    @staticmethod
    def prepare() -> None:
        Ants.get()
        Ants.check()
        Ants.get_top()

    @staticmethod
    def check() -> None:
        if not Ants.ants:
            Ants.populate(Config.default_population)

    @staticmethod
    def hatch(num: int = 1, ignore: list[str] | None = None) -> None:
        from .game import Game

        for _ in range(num):
            ant = Ant()
            ant.name = Ants.random_name(ignore)
            Ants.ants.append(ant)

            if Settings.verbose:
                Game.update(ant)

        Ants.on_change()

    @staticmethod
    def on_change() -> None:
        from .game import Game

        Ants.get_top()
        Game.info()
        Ants.save()

    @staticmethod
    def random_ant(ignore: list[Ant] | None = None) -> Ant | None:
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
    def get_next() -> Ant | None:
        now = Utils.now()
        ages = [(now - ant.updated) for ant in Ants.ants]

        # Normalize ages to create weights
        total_age = sum(ages)

        if total_age == 0:
            weights = [1] * len(Ants.ants)  # If all ages are zero, use equal weights
        else:
            weights = [
                int((age / total_age) * 1000) for age in ages
            ]  # Scale and cast to int

        # Perform weighted random selection
        return random.choices(Ants.ants, weights=weights, k=1)[0]

    @staticmethod
    def get_current() -> Ant | None:
        return max(Ants.ants, key=lambda ant: ant.updated)

    @staticmethod
    def set_status(ant: Ant, status: str, method: str) -> None:
        from .game import Game, Opts

        status = status.strip()
        ant.status = status
        ant.method = method
        ant.updated = Utils.now()

        Ants.on_change()

        if method in (Opts.triumph.method, Opts.hit.method):
            if not Settings.verbose:
                return

        Game.update(ant)

    @staticmethod
    def get() -> None:
        if Args.clean:
            objs = []
        else:
            objs = Storage.get_ants()

        for obj in objs:
            ant = Ant()
            ant.from_dict(obj)
            Ants.ants.append(ant)

    @staticmethod
    def populate(num: int) -> None:
        Ants.clear()
        Ants.hatch(num)

    @staticmethod
    def random_name(ignore: list[str] | None = None) -> str:
        names = Ants.get_names()

        if ignore:
            for name in ignore:
                if name not in names:
                    names.append(name)

        return Utils.random_name(names)

    @staticmethod
    def get_top() -> None:
        top: Ant | None = None
        top_score = 0

        for ant in Ants.ants:
            score = ant.get_score()

            if (not top) or (score > top_score):
                top = ant
                top_score = score
            elif score == top_score:
                if ant.created < top.created:
                    top = ant

        if not top:
            return

        Ants.top = top

    @staticmethod
    def merge(ant_1: Ant | None = None) -> bool:
        from .game import Game

        def split(ant: Ant) -> list[str]:
            return re.split(r"[ -]", ant.name)

        def remove(words: list[str], ignore: list[str]) -> list[str]:
            return [word for word in words if word.lower() not in ignore]

        def fill(words: list[str]) -> list[str]:
            words = remove(words, ["of", "de", "da", "the"])

            if len(words) < 2:
                n = random.randint(1, 2)

                if n == 1:
                    words = Utils.random_words(2 - len(words))
                else:
                    words = Utils.make_words(2 - len(words))

                words.extend(words)

            return [Utils.capitalize(word) for word in words]

        if not ant_1:
            ant_1 = Ants.random_ant()

        if not ant_1:
            return False

        ant_2 = Ants.random_ant([ant_1])

        if not ant_2:
            return False

        words_1 = split(ant_1)
        words_2 = split(ant_2)
        words_1 = fill(words_1)
        words_2 = fill(words_2)

        name = ""
        names = Ants.get_names()
        combinations = list(itertools.product(words_1, words_2))
        random.shuffle(combinations)

        for combo in combinations:
            possible = f"{combo[0]} {combo[1]}"

            if (possible == ant_1.name) or (possible == ant_2.name):
                continue

            if (possible in names) or (possible in Utils.names):
                continue

            name = possible
            break

        if not name:
            return False

        Ants.set_terminated(ant_1)
        Ants.set_terminated(ant_2)

        ant = Ant()
        ant.name = name
        ant.triumph = ant_1.triumph + ant_2.triumph
        ant.hits = ant_1.hits + ant_2.hits

        Ants.ants.append(ant)

        if Settings.verbose:
            Game.update(ant)

        Ants.hatch(ignore=[ant_1.name, ant_2.name])
        return True

    @staticmethod
    def clear() -> None:
        Ants.ants = []

    @staticmethod
    def terminate(ant: Ant) -> None:
        Ants.set_terminated(ant)
        Ants.hatch(ignore=[ant.name])

    @staticmethod
    def set_terminated(ant: Ant) -> None:
        from .game import Game

        ant.method = "terminated"

        if Settings.verbose:
            Game.update(ant)

        Ants.ants.remove(ant)
