from __future__ import annotations

import random
import colorsys
import time
from datetime import datetime
from typing import ClassVar

from fontTools.ttLib import TTFont  # type: ignore

from .config import Config
from .storage import Storage


class Utils:
    names: ClassVar[list[str]] = []

    @staticmethod
    def prepare() -> None:
        Utils.names = Storage.get_names()

    @staticmethod
    def now() -> float:
        return int(time.time())

    @staticmethod
    def singular_or_plural(num: float, singular: str, plural: str) -> str:
        if num == 1:
            return singular

        return plural

    @staticmethod
    def time_ago(start_time: float, end_time: float) -> str:
        diff = end_time - start_time
        seconds = int(diff)

        if seconds < 60:
            word = Utils.singular_or_plural(seconds, "second", "seconds")
            return f"{seconds} {word} ago"

        minutes = seconds // 60

        if minutes < 60:
            word = Utils.singular_or_plural(minutes, "minute", "minutes")
            return f"{minutes} {word} ago"

        hours = minutes / 60

        if hours < 24:
            word = Utils.singular_or_plural(hours, "hour", "hours")
            return f"{hours:.1f} {word} ago"

        days = hours / 24

        if days < 30:
            word = Utils.singular_or_plural(days, "day", "days")
            return f"{days:.1f} {word} ago"

        months = days / 30

        if months < 12:
            word = Utils.singular_or_plural(months, "month", "months")
            return f"{months:.1f} {word} ago"

        years = months / 12
        word = Utils.singular_or_plural(years, "year", "years")
        return f"{years:.1f} {word} ago"

    @staticmethod
    def print(text: str) -> None:
        print(text)  # noqa: T201

    @staticmethod
    def random_color(seed: str) -> tuple[int, int, int]:
        seed_int = hash(seed)
        random.seed(seed_int)

        h, s, l = (
            random.random(),
            0.5 + random.random() / 2.0,
            0.4 + random.random() / 5.0,
        )

        r, g, b = (int(256 * i) for i in colorsys.hls_to_rgb(h, l, s))
        return r, g, b

    @staticmethod
    def random_name() -> str:
        from .ants import Ants

        used = Ants.get_names()
        filtered = [name for name in Utils.names if name not in used]
        return random.choice(filtered)

    @staticmethod
    def get_rgb(color: tuple[int, int, int]) -> str:
        return f"rgb{color}"

    @staticmethod
    def get_random_character(font_path: str, num: int) -> str:
        font = TTFont(font_path)
        cmap = font["cmap"]
        unicode_map = cmap.getBestCmap()
        characters = [chr(code_point) for code_point in unicode_map]
        selected = random.sample(characters, num)
        return " ".join(selected)

    @staticmethod
    def get_random_emoji(num: int) -> str:
        return Utils.get_random_character(str(Config.emoji_font_path), num)

    @staticmethod
    def to_date(timestamp: float) -> str:
        dt_object = datetime.fromtimestamp(timestamp)
        hour = dt_object.strftime("%I").lstrip("0")
        return dt_object.strftime(f"%b %d %Y - {hour}:%M %p")