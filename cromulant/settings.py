from __future__ import annotations

from .window import Window
from .storage import Storage


class Settings:
    speed: str
    mode: str
    merge: bool

    score_enabled: bool
    travel_enabled: bool
    thoughts_enabled: bool
    words_enabled: bool

    @staticmethod
    def prepare() -> None:
        settings = Storage.get_settings()

        Settings.speed = settings.get("speed", "normal")
        speed = Settings.speed.capitalize()
        Window.speed.setCurrentText(speed)

        Settings.score_enabled = settings.get("score_enabled", True)
        Settings.travel_enabled = settings.get("travel_enabled", True)
        Settings.thoughts_enabled = settings.get("thoughts_enabled", True)
        Settings.words_enabled = settings.get("words_enabled", True)

        Settings.merge = settings.get("merge", True)

    @staticmethod
    def save() -> None:
        settings = {
            "speed": Settings.speed,
            "merge": Settings.merge,
            "score_enabled": Settings.score_enabled,
            "travel_enabled": Settings.travel_enabled,
            "thoughts_enabled": Settings.thoughts_enabled,
            "words_enabled": Settings.words_enabled,
        }

        Storage.save_settings(settings)

    @staticmethod
    def set_speed(speed: str) -> None:
        Settings.speed = speed
        Settings.save()

    @staticmethod
    def toggle_merge() -> None:
        Settings.merge = not Settings.merge
        Settings.save()

    @staticmethod
    def toggle_score_enabled() -> None:
        Settings.score_enabled = not Settings.score_enabled
        Settings.save()

    @staticmethod
    def toggle_travel_enabled() -> None:
        Settings.travel_enabled = not Settings.travel_enabled
        Settings.save()

    @staticmethod
    def toggle_thoughts_enabled() -> None:
        Settings.thoughts_enabled = not Settings.thoughts_enabled
        Settings.save()

    @staticmethod
    def toggle_words_enabled() -> None:
        Settings.words_enabled = not Settings.words_enabled
        Settings.save()

    @staticmethod
    def enable_all() -> None:
        Settings.score_enabled = True
        Settings.travel_enabled = True
        Settings.thoughts_enabled = True
        Settings.words_enabled = True
        Settings.save()

    @staticmethod
    def disable_all() -> None:
        Settings.score_enabled = False
        Settings.travel_enabled = False
        Settings.thoughts_enabled = False
        Settings.words_enabled = False
        Settings.save()