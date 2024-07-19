from pathlib import Path

import appdirs  # type: ignore


class Config:
    title = "Cromulant"
    width = 800
    height = 600
    max_ants = 100
    here: str
    ants_json: Path
    icon_path: Path
    image_path: Path
    names_json: Path


    @staticmethod
    def prepare() -> None:
        Config.here = Path(__file__).parent
        Config.ants_json = Path(appdirs.user_data_dir()) / "cromulant" / "ants.json"

        if not Config.ants_json.exists():
            Config.ants_json.parent.mkdir(parents=True, exist_ok=True)
            Config.ants_json.write_text("[]")

        Config.icon_path = Config.here / "img" / "icon_4.jpg"
        Config.image_path = Config.here / "img" / "icon_7.jpg"
        Config.names_json = Config.here / "data" / "names.json"