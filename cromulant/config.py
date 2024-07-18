from pathlib import Path


class Config:
    title = "Cromulant"
    width = 800
    height = 600
    here: str
    database_path: Path
    schema_path: Path


    @staticmethod
    def prepare() -> None:
        Config.here = Path(__file__).parent
        Config.database_path = Config.here / "cromulant.db"
        Config.schema_path = Config.here / "schema.sql"