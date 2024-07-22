from __future__ import annotations

from .window import Window
from .storage import Storage


class Settings:
    speed: str
    mode: str

    @staticmethod
    def prepare() -> None:
        settings = Storage.get_settings()

        Settings.speed = settings.get("speed", "normal")
        speed = Settings.speed.capitalize()
        Window.speed.setCurrentText(speed)

        Settings.mode = settings.get("mode", "all")
        mode = Settings.mode.capitalize()
        Window.mode.setCurrentText(mode)

    @staticmethod
    def save() -> None:
        settings = {
            "speed": Settings.speed,
            "mode": Settings.mode,
        }

        Storage.save_settings(settings)

    @staticmethod
    def set_speed(speed: str) -> None:
        Settings.speed = speed
        Settings.save()

    @staticmethod
    def set_mode(mode: str) -> None:
        Settings.mode = mode
        Settings.save()
