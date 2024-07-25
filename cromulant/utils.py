from __future__ import annotations

import random
import colorsys
import time
from datetime import datetime
from typing import ClassVar

from wonderwords import RandomWord, RandomSentence  # type: ignore
from fontTools.ttLib import TTFont  # type: ignore

from .config import Config


class Utils:
    names: ClassVar[list[str]] = []
    countries: ClassVar[list[str]] = []
    rand_word: RandomWord
    rand_sentence: RandomSentence
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"

    @staticmethod
    def prepare() -> None:
        from .storage import Storage

        Utils.names = Storage.get_names()
        Utils.countries = Storage.get_countries()
        Utils.rand_word = RandomWord()
        Utils.rand_sentence = RandomSentence()

    @staticmethod
    def now() -> int:
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
    def random_name(ignore: list[str], include: list[str] | None = None) -> str:
        names = Utils.names

        if include:
            for name in include:
                if name not in names:
                    names.append(name)

        filtered = [name for name in Utils.names if name not in ignore]

        if not filtered:
            return Utils.make_name()

        return random.choice(filtered)

    @staticmethod
    def get_rgb(color: tuple[int, int, int]) -> str:
        return f"rgb{color}"

    @staticmethod
    def random_character(font_path: str, num: int) -> str:
        font = TTFont(font_path)
        cmap = font["cmap"]
        unicode_map = cmap.getBestCmap()
        characters = [chr(code_point) for code_point in unicode_map]

        for _ in range(10):  # Try up to 10 times
            selected = random.sample(characters, num)

            if all((char.isprintable() and not char.isspace()) for char in selected):
                return " ".join(selected)

        return ""

    @staticmethod
    def random_emoji(num: int) -> str:
        return Utils.random_character(str(Config.emoji_font_path), num)

    @staticmethod
    def to_date(timestamp: float) -> str:
        dt_object = datetime.fromtimestamp(timestamp)
        hour = dt_object.strftime("%I").lstrip("0")
        return dt_object.strftime(f"%b %d %Y - {hour}:%M %p")

    @staticmethod
    def get_seconds(msecs: int) -> str:
        seconds = msecs // 1000

        if seconds < 60:
            return f"{seconds} seconds"

        minutes = seconds // 60

        if minutes == 1:
            return "1 minute"

        return f"{minutes} minutes"

    @staticmethod
    def random_country(ignore: list[str]) -> str:
        filtered = [country for country in Utils.countries if country not in ignore]
        return random.choice(filtered)

    @staticmethod
    def random_word(num: int = 1) -> list[str]:
        words = []

        for _ in range(num):
            word = Utils.rand_word.word(
                include_parts_of_speech=["nouns", "adjectives"], word_max_length=8
            )

            words.append(word)

        return words

    @staticmethod
    def capitalize(word: str) -> str:
        return word[0].upper() + word[1:]

    @staticmethod
    def words_1() -> str:
        return str(Utils.rand_sentence.simple_sentence())

    @staticmethod
    def words_2() -> str:
        return str(Utils.rand_sentence.bare_bone_sentence())

    @staticmethod
    def words_3() -> str:
        return str(Utils.rand_sentence.bare_bone_with_adjective())

    @staticmethod
    def words_4() -> str:
        return str(Utils.rand_sentence.sentence())

    @staticmethod
    def make_word() -> str:
        name = ""
        name += random.choice(Utils.consonants)
        name += random.choice(Utils.vowels)
        name += random.choice(Utils.consonants)
        name += random.choice(Utils.vowels)
        return name

    @staticmethod
    def make_name() -> str:
        word_1 = Utils.make_word()
        word_2 = Utils.make_word()

        return f"{Utils.capitalize(word_1)} {Utils.capitalize(word_2)}"
