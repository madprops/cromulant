from __future__ import annotations

from pathlib import Path

import appdirs  # type: ignore


class Config:
    title: str = "Cromulant"
    program: str = "cromulant"
    width: int = 820
    height: int = 900
    max_ants: int = 100
    here: Path
    ants_json: Path
    icon_path: Path
    status_image_path: Path
    hatched_image_path: Path
    terminated_image_path: Path
    names_json: Path
    background_color: str = "rgb(44, 44, 44)"
    text_color: str = "#ffffff"
    image_size: int = 80
    space_1: int = 20
    max_messages: int = 200
    loop_delay_fast: int = 1000 * 5
    loop_delay_normal: int = 1000 * 60 * 1
    loop_delay_slow: int = 1000 * 60 * 5
    hatch_burst: int = 3
    font_size: int = 20
    info_separator: str = "  -  "
    font_path: Path
    emoji_font_path: Path
    triumph_color: tuple[int, int, int] = (255, 255, 0)
    hit_color: tuple[int, int, int] = (255, 0, 77)
    triumph_icon: str = "😀"
    hit_icon: str = "🎃"
    triumph_message: str = "Scored a triumph"
    hit_message: str = "Took a hit"
    song_path: Path
    logo_path: Path
    alt_background_color: str = "rgb(33, 33, 33)"
    alt_text_color: str = "white"
    alt_hover_background_color: str = "rgb(51, 51, 51)"
    alt_hover_text_color: str = "white"
    alt_border_color: str = "rgb(88, 88, 88)"
    message_box_button_hover_background_color: str = "rgb(66, 66, 66)"
    message_box_button_hover_text_color: str = "white"
    scrollbar_handle_color: str = "rgb(69, 69, 69)"
    input_background_color: str = "rgb(111, 111, 111)"
    input_text_color: str = "rgb(18, 18, 18)"
    input_border_color: str = "rgb(140, 140, 140)"
    input_caret_color: str = "rgb(18, 18, 18)"
    settings_json: Path

    @staticmethod
    def prepare() -> None:
        Config.here = Path(__file__).parent
        Config.ants_json = Path(appdirs.user_data_dir()) / "cromulant" / "ants.json"

        if not Config.ants_json.exists():
            Config.ants_json.parent.mkdir(parents=True, exist_ok=True)
            Config.ants_json.write_text("[]")

        Config.settings_json = (
            Path(appdirs.user_config_dir()) / "cromulant" / "settings.json"
        )

        if not Config.settings_json.exists():
            Config.settings_json.parent.mkdir(parents=True, exist_ok=True)
            Config.settings_json.write_text("{}")

        Config.icon_path = Config.here / "img" / "icon_4.jpg"
        Config.status_image_path = Config.here / "img" / "icon_5.jpg"
        Config.hatched_image_path = Config.here / "img" / "icon_7.jpg"
        Config.terminated_image_path = Config.here / "img" / "icon_6.jpg"
        Config.names_json = Config.here / "data" / "names.json"
        Config.font_path = Config.here / "fonts" / "NotoSans-Regular.ttf"
        Config.emoji_font_path = Config.here / "fonts" / "NotoEmoji-Regular.ttf"
        Config.song_path = Config.here / "audio" / "March of the Cyber Ants.mp3"
        Config.logo_path = Config.here / "img" / "logo_3.jpg"
