from __future__ import annotations

from pathlib import Path

import appdirs  # type: ignore


class Config:
    title: str = "Cromulant"
    width: int = 900
    height: int = 800
    max_ants: int = 100
    here: Path
    ants_json: Path
    icon_path: Path
    status_image_path: Path
    hatched_image_path: Path
    terminated_image_path: Path
    names_json: Path
    background_color: str = "#2c2c2c"
    text_color: str = "#ffffff"
    image_size: int = 80
    space_1: int = 25
    max_messages: int = 120
    loop_delay_fast: int = 3_000
    loop_delay_normal: int = 20_000
    loop_delay_slow: int = 60_000
    hatch_burst: int = 3

    @staticmethod
    def prepare() -> None:
        Config.here = Path(__file__).parent
        Config.ants_json = Path(appdirs.user_data_dir()) / "cromulant" / "ants.json"

        if not Config.ants_json.exists():
            Config.ants_json.parent.mkdir(parents=True, exist_ok=True)
            Config.ants_json.write_text("[]")

        Config.icon_path = Config.here / "img" / "icon_4.jpg"
        Config.status_image_path = Config.here / "img" / "icon_5.jpg"
        Config.hatched_image_path = Config.here / "img" / "icon_7.jpg"
        Config.terminated_image_path = Config.here / "img" / "icon_6.jpg"
        Config.names_json = Config.here / "data" / "names.json"
