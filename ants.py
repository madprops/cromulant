from __future__ import annotations

import utils
from database import Database

class Ant:
    def __init__(self) -> None:
        now = utils.now()
        self.id: int
        self.created = now
        self.updated = now
        self.name = ""
        self.status = ""
        self.hits = 0
        self.triumph = 0

    def get_name(self):
        return self.name or "Nameless"

    def get_age(self):
        now = utils.now()
        return utils.time_ago(self.created, now)

    def describe(self):
        print(f"Name is {self.get_name()}")
        print(f"It hatched {self.get_age()}")

class Ants:
    ants: list[Ant] = []

    @staticmethod
    def get_all() -> None:
        Database.cursor.execute("SELECT id, created, updated, name, status, hits, triumph FROM ants")

        rows = Database.cursor.fetchall()
        ants = []

        for row in rows:
            ant = Ant()
            ant.id = row[0]
            ant.created = row[1]
            ant.updated = row[2]
            ant.name = row[3]
            ant.status = row[4]
            ant.hits = row[5]
            ant.triumph = row[6]
            ants.append(ant)

        Database.connection.commit()
        return ants

    @staticmethod
    def hatch() -> None:
        now = utils.now()

        Database.cursor.execute(
            "INSERT INTO ants (created, updated) VALUES (?, ?)",
            (now, now),
        )

        Database.connection.commit()
        Database.cursor.execute("SELECT last_insert_rowid()")
        row = Database.cursor.fetchone()

        ant = Ant()
        ant.id = row[0]

        print(f"Ant hatched: {ant.id}")