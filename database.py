from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    @staticmethod
    def prepare() -> None:
        Database.connection = sqlite3.connect("ants.db")
        Database.cursor = Database.connection.cursor()

    @staticmethod
    def create() -> None:
        with Path("schema.sql").open("r") as file:
            schema = file.read()

        Database.cursor.executescript(schema)
        Database.connection.commit()
