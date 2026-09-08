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
    if config_path is not None:
        test_root = config_path.resolve().parent
    else:
        test_root = Path(__file__).resolve().parents[2]
    test_path = test_root / "tests" / "mediatests"
    return pytest.main([str(test_path), "--rootdir", str(test_root)])
