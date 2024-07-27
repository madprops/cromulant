from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .config import Config
from .utils import Utils
from .argspec import ArgSpec


class Args:
    names: Path | None = None
    ants: Path | None = None
    images: bool = True
    header: bool = True
    footer: bool = True
    intro: bool = True
    title: str = ""
    width: int = 0
    height: int = 0
    program: str = ""
    speed: str = ""
    clean: bool = False
    fast_minutes: float = 0.0
    normal_minutes: float = 0.0
    slow_minutes: float = 0.0
    argdoc: bool = False
    score: bool = False
    mono: bool = False

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
            "width",
            "height",
            "program",
            "speed",
            "clean",
            "fast_minutes",
            "normal_minutes",
            "slow_minutes",
            "argdoc",
            "score",
            "mono",
        ]

        for n_item in normals:
            ArgParser.get_value(n_item)

        paths = [
            "names",
            "ants",
        ]

        for p_item in paths:
            ArgParser.get_value(p_item, path=True)

    @staticmethod
    def make_argdoc() -> None:
        from .utils import Utils
        from .storage import Storage

        text = Args.argtext()
        Storage.save_arguments(text)
        Utils.print("Saved arguments document")

    @staticmethod
    def argtext(filter_text: str | None = None) -> str:
        sep = "\n\n---\n\n"
        text = ""
        filter_lower = ""

        if not filter_text:
            text = "# Arguments\n\n"
            text += "Here are all the available command line arguments:"
        else:
            filter_lower = filter_text.lower()

        for key in ArgSpec.arguments:
            if key == "string_arg":
                continue

            arg = ArgSpec.arguments[key]
            info = arg.get("help", "")

            if filter_text:
                if filter_lower not in key.lower():
                    if filter_lower not in info.lower():
                        continue

            text += sep
            name = key.replace("_", "-")
            text += f"### {name}"

            if info:
                text += "\n\n"
                text += info

            defvalue = ArgSpec.defaults.get(key)

            if defvalue is not None:
                if isinstance(defvalue, str):
                    if defvalue == "":
                        defvalue = "[Empty string]"
                    elif defvalue.strip() == "":
                        spaces = defvalue.count(" ")
                        ds = Utils.singular_or_plural(spaces, "space", "spaces")
                        defvalue = f"[{spaces} {ds}]"
                    else:
                        defvalue = f'"{defvalue}"'

                text += "\n\n"
                text += f"Default: {defvalue}"

            choices = arg.get("choices", [])

            if choices:
                text += "\n\n"
                text += "Choices: "

                choicestr = [
                    f'"{choice}"' if isinstance(choice, str) else choice
                    for choice in choices
                ]

                text += ", ".join(choicestr)

            action = arg.get("action", "")

            if action:
                text += "\n\n"
                text += f"Action: {action}"

            argtype = arg.get("type", "")

            if argtype:
                text += "\n\n"
                text += f"Type: {argtype.__name__}"

        text += "\n"
        return text.lstrip()


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
