from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from .config import Config

if TYPE_CHECKING:
    from .ants import Ant


class Storage:
    @staticmethod
    def get_ants() -> Any:
        with Config.ants_json.open() as file:
            return json.load(file)

    @staticmethod
    def save_ants(ants: list[Ant]) -> None:
        objs = [ant.to_dict() for ant in ants]

        with Config.ants_json.open("w") as file:
            json.dump(objs, file)

    @staticmethod
    def get_names() -> Any:
        with Config.names_json.open() as file:
            return json.load(file)

    @staticmethod
    def get_settings() -> Any:
        with Config.settings_json.open() as file:
            return json.load(file)

    @staticmethod
    def save_settings(settings: dict[str, Any]) -> None:
        with Config.settings_json.open("w") as file:
            json.dump(settings, file)

    @staticmethod
    def get_countries() -> Any:
        with Config.countries_json.open() as file:
            return json.load(file)
