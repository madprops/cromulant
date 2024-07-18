from __future__ import annotations
from typing import ClassVar

from .utils import Utils
from .database import Database


class Ant:
    def __init__(self) -> None:
        now = Utils.now()
        self.id: int
        self.created = now
        self.updated = now
        self.name = ""
        self.status = ""
        self.hits = 0
        self.triumph = 0

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
    def get_all() -> None:
        Database.cursor.execute(
            "SELECT id, created, updated, name, status, hits, triumph FROM ants"
        )
        rows = Database.cursor.fetchall()

        for row in rows:
            ant = Ant()
            ant.id = row[0]
            ant.created = row[1]
            ant.updated = row[2]
            ant.name = row[3]
            ant.status = row[4]
            ant.hits = row[5]
            ant.triumph = row[6]
            Ants.ants.append(ant)

    @staticmethod
    def hatch() -> None:
        now = Utils.now()

        Database.cursor.execute(
            "INSERT INTO ants (created, updated) VALUES (?, ?)",
            (now, now),
        )

        Database.connection.commit()
        Database.cursor.execute("SELECT last_insert_rowid()")
        row = Database.cursor.fetchone()

        ant = Ant()
        ant.id = row[0]

        Utils.print(f"Ant hatched: {ant.id}")

    @staticmethod
    def terminate() -> None:
        pass
