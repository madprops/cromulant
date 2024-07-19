import json
from typing import TYPE_CHECKING

from .config import Config

if TYPE_CHECKING:
    from .ants import Ant


class Storage:
    @staticmethod
    def get_ants() -> None:
        with Config.ants_json.open() as file:
            return json.load(file)

    @staticmethod
    def save_ants(ants: list["Ant"]) -> None:
        objs = [ant.to_dict() for ant in ants]

        with Config.ants_json.open("w") as file:
            json.dump(objs, file)

    @staticmethod
    def get_names() -> None:
        with Config.names_json.open() as file:
            return json.load(file)