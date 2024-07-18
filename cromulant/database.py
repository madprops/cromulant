from __future__ import annotations

import sqlite3
from pathlib import Path

from .config import Config


class Database:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    @staticmethod
    def prepare() -> None:
        Database.connection = sqlite3.connect(Config.database_path)
        Database.cursor = Database.connection.cursor()

    @staticmethod
    def create() -> None:
        with Config.schema_path.open("r") as file:
            schema = file.read()

        Database.cursor.executescript(schema)
        Database.connection.commit()
