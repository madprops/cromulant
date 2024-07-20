from __future__ import annotations

from .window import Window
from .storage import Storage


class Settings:
    speed: str

    @staticmethod
    def prepare() -> None:
        settings = Storage.get_settings()
        Settings.speed = settings.get("speed", "normal")
        speed = Settings.speed.capitalize()
        Window.speed.setCurrentText(speed)

    @staticmethod
    def save() -> None:
        settings = {
            "speed": Settings.speed,
        }

        Storage.save_settings(settings)

    @staticmethod
    def set_speed(speed: str) -> None:
        Settings.speed = speed
        Settings.save()
