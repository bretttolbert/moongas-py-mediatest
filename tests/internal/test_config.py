import shutil
from pathlib import Path

from mediatest.config import MediaTestConfigUtil


def test_load_config_from_path(tmp_path: Path):
    source_config_path = Path(__file__).resolve().parents[2] / "mediatest-config.yaml"
    config_directory = tmp_path / "config"
    config_directory.mkdir()
    config_path = config_directory / source_config_path.name
    shutil.copy(source_config_path, config_path)

    config = MediaTestConfigUtil().load_config(config_path)

    assert len(config.libs) == 2
    assert config.libs[0].media_path == "/data/Music/"
    assert config.libs[0].expected_media_count == 21666
    assert config.libs[1].media_path == "/data/MusicOther/"
    assert config.libs[1].expected_media_count == 0