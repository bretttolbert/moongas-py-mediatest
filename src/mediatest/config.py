from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
import sys

from dataclass_wizard.v0 import YAMLWizard
from mediascan.genres import Genre


@dataclass
class MediaTestLibConfig(YAMLWizard):
    media_path: str
    expected_media_count: int
    expected_lrc_count: int
    total_filesize_limit_gb: int
    expected_filesize_gb: int
    genres: list[Genre]


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
    libs: list[MediaTestLibConfig]


class MediaTestConfigUtil:
    """Utility class for loading mediatest configuration from YAML."""

    yaml_filename = "mediatest-config.yml"

    def load_config(self, path: Path | None = None) -> MediaTestConfig:
        if path is not None:
            config_path = path
            if not config_path.exists():
                raise Exception(f"The provided mediatest config file path does not exist: path={path} cwd={os.getcwd()}")
        else:
            source_config_path = Path(__file__).resolve().parents[2] / self.yaml_filename
            config_path = source_config_path if source_config_path.exists() else Path(sys.prefix) / self.yaml_filename
        with config_path.open("r", encoding="utf-8") as config_file:
            config = MediaTestConfig.from_yaml(config_file)  # pyright: ignore[reportUnknownMemberType]
        if isinstance(config, list):
            return config[0]
        return config


def configure(path: Path | None = None) -> None:
    global CONFIG
    global MEDIASCAN_FILES_PATH, MINIMUM_FILESIZE
    global EXTS_MEDIA, EXTS_ART, EXTS_LYRICS, EXTS_METADATA, EXTS_EXTRA, ALLOWED_EXTS
    global LIB_GENRES_MODE_BLACKLIST, LIB_COUNT, LIBS_MEDIA_PATH
    global LIBS_EXPECTED_MEDIA_COUNT, LIBS_EXPECTED_LRC_COUNT
    global LIBS_TOTAL_FILESIZE_LIMIT_GB, LIBS_EXPECTED_FILESIZE_GB, LIBS_GENRES

    CONFIG = MediaTestConfigUtil().load_config(path)
    MEDIASCAN_FILES_PATH = CONFIG.mediascan_files_path
    MINIMUM_FILESIZE = CONFIG.minimum_filesize
    EXTS_MEDIA = CONFIG.exts_media
    EXTS_ART = CONFIG.exts_art
    EXTS_LYRICS = CONFIG.exts_lyrics
    EXTS_METADATA = CONFIG.exts_metadata
    EXTS_EXTRA = CONFIG.exts_extra
    ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_LYRICS + EXTS_METADATA + EXTS_EXTRA
    LIB_GENRES_MODE_BLACKLIST = CONFIG.lib_genres_mode_blacklist
    LIB_COUNT = len(CONFIG.libs)
    LIBS_MEDIA_PATH = [lib.media_path for lib in CONFIG.libs]
    LIBS_EXPECTED_MEDIA_COUNT = [lib.expected_media_count for lib in CONFIG.libs]
    LIBS_EXPECTED_LRC_COUNT = [lib.expected_lrc_count for lib in CONFIG.libs]
    LIBS_TOTAL_FILESIZE_LIMIT_GB = [lib.total_filesize_limit_gb for lib in CONFIG.libs]
    LIBS_EXPECTED_FILESIZE_GB = [lib.expected_filesize_gb for lib in CONFIG.libs]
    LIBS_GENRES = [lib.genres for lib in CONFIG.libs]


PRESENT_YEAR: int = datetime.now().year
configure()
