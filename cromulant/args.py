from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .config import Config
from .argspec import ArgSpec


class Args:
    names: Path | None = None
    images: bool = True
    header: bool = True
    footer: bool = True
    intro: bool = True
    title: str = ""

    @staticmethod
    def prepare() -> None:
        ArgSpec.prepare()
        ArgParser.prepare(Config.title, ArgSpec.arguments)

        for attr_name, attr_value in vars(Args).items():
            ArgSpec.defaults[attr_name] = attr_value

        other_name = [
            ("no_images", "images"),
            ("no_header", "header"),
            ("no_footer", "footer"),
            ("no_intro", "intro"),
        ]

        for r_item in other_name:
            ArgParser.get_value(*r_item)

        normals = [
            "title",
        ]

        for n_item in normals:
            ArgParser.get_value(n_item)

        paths = [
            "names",
        ]

        for p_item in paths:
            ArgParser.get_value(p_item, path=True)


class ArgParser:
    parser: argparse.ArgumentParser
    args: argparse.Namespace

    @staticmethod
    def prepare(title: str, argdefs: dict[str, Any]) -> None:
        parser = argparse.ArgumentParser(description=title)
        argdefs["string_arg"] = {"nargs": "*"}

        for key in argdefs:
            item = argdefs[key]

            if key == "string_arg":
                name = key
            else:
                name = ArgParser.under_to_dash(key)
                name = f"--{name}"

            tail = {key: value for key, value in item.items() if value is not None}
            parser.add_argument(name, **tail)

        ArgParser.parser = parser
        ArgParser.args = parser.parse_args()

    @staticmethod
    def string_arg() -> str:
        return " ".join(ArgParser.args.string_arg)

    @staticmethod
    def get_value(
        attr: str, key: str | None = None, no_strip: bool = False, path: bool = False
    ) -> None:
        value = getattr(ArgParser.args, attr)

        if value is not None:
            if not no_strip:
                if isinstance(value, str):
                    value = value.strip()

            obj = key if key else attr

            if path:
                value = Path(value)

            ArgParser.set(obj, value)

    @staticmethod
    def set(attr: str, value: Any) -> None:
        setattr(Args, attr, value)

    @staticmethod
    def under_to_dash(s: str) -> str:
        return s.replace("_", "-")
