import argparse
from pathlib import Path

import pytest

from mediatest.config import configure


def main(config_path: Path | None = None) -> int:
    if config_path is None:
        parser = argparse.ArgumentParser()
        parser.add_argument("config_path", type=Path, nargs="?")
        config_path = parser.parse_args().config_path

    configure(config_path)
    return pytest.main(["tests/mediatests"])
