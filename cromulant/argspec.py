from __future__ import annotations

from typing import Any

from .config import Config


class DuplicateArgumentError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Duplicate argument: {key}"

    def __str__(self) -> str:
        return self.message


class MissingInfoError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Missing info for argument: {key}"

    def __str__(self) -> str:
        return self.message


class DuplicateInfoError(Exception):
    def __init__(self, key: str) -> None:
        self.message = f"Duplicate info for argument: {key}"

    def __str__(self) -> str:
        return self.message


class ArgSpec:
    vinfo: str
    defaults: dict[str, Any]
    arguments: dict[str, Any]
    infos: list[str]

    @staticmethod
    def prepare() -> None:
        ArgSpec.vinfo = f"{Config.title} {Config.version}"
        ArgSpec.defaults = {}
        ArgSpec.arguments = {}
        ArgSpec.infos = []
        ArgSpec.add_arguments()

    @staticmethod
    def add_argument(key: str, info: str, **kwargs: Any) -> None:
        if key in ArgSpec.arguments:
            raise DuplicateArgumentError(key)

        if not info:
            raise MissingInfoError(key)

        if info in ArgSpec.infos:
            raise DuplicateInfoError(key)

        ArgSpec.arguments[key] = {
            "help": info,
            **kwargs,
        }

        ArgSpec.infos.append(info)

    @staticmethod
    def add_arguments() -> None:
        ArgSpec.add_argument(
            "version",
            action="version",
            info="Check the version of the program",
            version=ArgSpec.vinfo,
        )

        ArgSpec.add_argument(
            "names",
            type=str,
            info="Path to a JSON file with a list of names. Use these instead of the default ones",
        )

        ArgSpec.add_argument(
            "ants",
            type=str,
            info="Path to a JSON file with ants data. Use this instead of the default one",
        )

        ArgSpec.add_argument(
            "no_images",
            action="store_false",
            info="Don't show the images on the left",
        )

        ArgSpec.add_argument(
            "no_header",
            action="store_false",
            info="Don't show the header controls",
        )

        ArgSpec.add_argument(
            "no_footer",
            action="store_false",
            info="Don't show the footer controls",
        )

        ArgSpec.add_argument(
            "no_intro",
            action="store_false",
            info="Don't show the intro message",
        )

        ArgSpec.add_argument(
            "title",
            type=str,
            info="Custom title for the window",
        )

        ArgSpec.add_argument(
            "width",
            type=int,
            info="The width of the window in pixels",
        )

        ArgSpec.add_argument(
            "height",
            type=int,
            info="The height of the window in pixels",
        )

        ArgSpec.add_argument(
            "program",
            type=str,
            info="The internal name of the program",
        )

        ArgSpec.add_argument(
            "speed",
            type=str,
            choices=["fast", "normal", "slow"],
            info="Use this update speed",
        )

        ArgSpec.add_argument(
            "clean",
            action="store_true",
            info="Start with clean ants data",
        )

        ArgSpec.add_argument(
            "fast_minutes",
            type=float,
            info="The number of minutes between fast updates",
        )

        ArgSpec.add_argument(
            "normal_minutes",
            type=float,
            info="The number of minutes between normal updates",
        )

        ArgSpec.add_argument(
            "slow_minutes",
            type=float,
            info="The number of minutes between slow updates",
        )

        ArgSpec.add_argument(
            "argdoc",
            action="store_true",
            info="Make the arguments document and exit",
        )
