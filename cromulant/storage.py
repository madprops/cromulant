from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any
from pathlib import Path

from .config import Config

if TYPE_CHECKING:
    from .ants import Ant

from .args import Args
from .utils import Utils


class Storage:
    @staticmethod
    def get_names_path() -> Path:
        path = Config.names_json

        if Args.names:
            if Args.names.exists():
                path = Args.names

        return path

    @staticmethod
    def get_ants_path() -> Path:
        path = Config.ants_json

        if Args.ants:
            if Args.ants.exists():
                path = Args.ants

        return path

    @staticmethod
    def get_ants() -> Any:
        try:
            path = Storage.get_ants_path()

            with path.open() as file:
                return json.load(file)
        except Exception as e:
            Utils.print(str(e))
            return []

    @staticmethod
    def save_ants(ants: list[Ant]) -> None:
        objs = [ant.to_dict() for ant in ants]
        path = Storage.get_ants_path()

        with path.open("w") as file:
            json.dump(objs, file)

    @staticmethod
    def get_names() -> Any:
        path = Storage.get_names_path()

        with path.open() as file:
            return json.load(file)

    @staticmethod
    def get_settings() -> Any:
        try:
            with Config.settings_json.open() as file:
                return json.load(file)
        except Exception as e:
            Utils.print(str(e))
            return {}

    @staticmethod
    def save_settings(settings: dict[str, Any]) -> None:
        with Config.settings_json.open("w") as file:
            json.dump(settings, file)

    @staticmethod
    def get_countries() -> Any:
        with Config.countries_json.open() as file:
            return json.load(file)

    @staticmethod
    def get_manifest() -> Any:
        with Config.manifest_path.open() as file:
            return json.load(file)
