from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from dataclass_wizard.v0 import YAMLWizard
from mediascan.genres import Genre


@dataclass
class MediaTestConfig(YAMLWizard):
    mediascan_files_path: str
    minimum_filesize: int
    exts_media: list[str]
    exts_art: list[str]
    exts_lyrics: list[str]
    exts_metadata: list[str]
    exts_extra: list[str]
    lib_genres_mode_blacklist: bool
    libs_media_path: list[str]
    libs_expected_media_count: list[int]
    libs_expected_lrc_count: list[int]
    libs_total_filesize_limit_gb: list[int]
    libs_expected_filesize_gb: list[int]
    libs_genres: list[list[Genre]]


class MediaTestConfigUtil:
    """Utility class for loading mediatest configuration from YAML."""

    yaml_filename = "mediatest-config.yaml"

    def load_config(self, path: Path | None = None) -> MediaTestConfig:
        config_path = path or Path(__file__).with_name(self.yaml_filename)
        with config_path.open("r", encoding="utf-8") as config_file:
            config = MediaTestConfig.from_yaml(config_file)  # pyright: ignore[reportUnknownMemberType]
        if isinstance(config, list):
            return config[0]
        return config


CONFIG = MediaTestConfigUtil().load_config()

MEDIASCAN_FILES_PATH = CONFIG.mediascan_files_path
PRESENT_YEAR: int = datetime.now().year
MINIMUM_FILESIZE = CONFIG.minimum_filesize
EXTS_MEDIA = CONFIG.exts_media
EXTS_ART = CONFIG.exts_art
EXTS_LYRICS = CONFIG.exts_lyrics
EXTS_METADATA = CONFIG.exts_metadata
EXTS_EXTRA = CONFIG.exts_extra
ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_LYRICS + EXTS_METADATA + EXTS_EXTRA

LIB_GENRES_MODE_BLACKLIST = CONFIG.lib_genres_mode_blacklist
LIB_COUNT = len(CONFIG.libs_media_path)
LIBS_MEDIA_PATH = CONFIG.libs_media_path
LIBS_EXPECTED_MEDIA_COUNT = CONFIG.libs_expected_media_count
LIBS_EXPECTED_LRC_COUNT = CONFIG.libs_expected_lrc_count
LIBS_TOTAL_FILESIZE_LIMIT_GB = CONFIG.libs_total_filesize_limit_gb
LIBS_EXPECTED_FILESIZE_GB = CONFIG.libs_expected_filesize_gb
LIBS_GENRES = CONFIG.libs_genres
