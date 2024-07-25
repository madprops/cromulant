from __future__ import annotations

from pathlib import Path

import appdirs  # type: ignore


class Config:
    program: str
    title: str
    version: str
    width: int = 820
    height: int = 900
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
    space_1: int = 18
    max_updates: int = 300
    loop_delay_fast: int = 1000 * 5
    loop_delay_normal: int = 1000 * 60 * 1
    loop_delay_slow: int = 1000 * 60 * 5
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
    input_border_color: str = "rgb(120, 120, 120)"
    input_caret_color: str = "rgb(18, 18, 18)"
    settings_json: Path
    countries_json: Path
    filter_debouncer_delay: int = 200
    default_population: int = 100
    merge_goal: int = 10
    manifest_path: Path
    manifest: dict[str, str]
    icon_on: str = "✅"
    icon_off: str = "❌"
    ant: str = "🐜"

    @staticmethod
    def prepare() -> None:
        from .storage import Storage

        Config.here = Path(__file__).parent
        Config.manifest_path = Config.here / "manifest.json"
        Config.manifest = Storage.get_manifest()
        Config.title = Config.manifest["title"]
        Config.program = Config.manifest["program"]
        Config.version = Config.manifest["version"]

        Config.ants_json = Path(appdirs.user_data_dir()) / Config.program / "ants.json"

        if not Config.ants_json.exists():
            Config.ants_json.parent.mkdir(parents=True, exist_ok=True)
            Config.ants_json.write_text("[]")

        Config.settings_json = (
            Path(appdirs.user_config_dir()) / Config.program / "settings.json"
        )

        if not Config.settings_json.exists():
            Config.settings_json.parent.mkdir(parents=True, exist_ok=True)
            Config.settings_json.write_text("{}")

        Config.names_json = Config.here / "data" / "names.json"
        Config.countries_json = Config.here / "data" / "countries.json"
        Config.icon_path = Config.here / "img" / "icon_1.jpg"
        Config.status_image_path = Config.here / "img" / "icon_2.jpg"
        Config.hatched_image_path = Config.here / "img" / "hatched.jpg"
        Config.terminated_image_path = Config.here / "img" / "terminated.jpg"
        Config.font_path = Config.here / "fonts" / "NotoSans-Regular.ttf"
        Config.emoji_font_path = Config.here / "fonts" / "NotoEmoji-Regular.ttf"
        Config.song_path = Config.here / "audio" / "March of the Cyber Ants.mp3"
        Config.logo_path = Config.here / "img" / "logo_3.jpg"
