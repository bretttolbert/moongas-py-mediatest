import argparse
import hashlib
import logging
import sys
from pathlib import Path

import pytest

from mediatest.config import configure, MEDIATEST_ROOTDIR

logger = logging.getLogger(__name__)


def file_hash_sha256(file_path: Path):
    with open(file_path, "rb") as f:
        return hashlib.file_digest(f, "sha256")

def main() -> int:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger.debug("main() starting")
    logger.debug("sys.argv before parsing: %s", sys.argv)

    parser = argparse.ArgumentParser(
        description="Run mediatest media tests using the provided config YAML file",
    )
    parser.add_argument(
        "config_path",
        type=Path,
        help="Path to the mediatest config YAML file.",
    )
    args = parser.parse_args()
    logger.debug("argparse parsed args: %s", args)

    config_path = args.config_path
    logger.info("Received CLI config path: %s", config_path)
    logger.debug("config_path raw value: %r", config_path)
    logger.debug("config_path absolute form before exists check: %s", config_path.absolute())
    logger.debug("config_path resolved form before exists check: %s", config_path.resolve())

    logger.debug("Checking whether config file exists at %s", config_path)
    logger.debug("os.path.exists(%s) = %s", config_path, config_path.exists())
    logger.debug("is_file(%s) = %s", config_path, config_path.is_file())

    if not config_path.exists():
        logger.error("Config file missing: %s", config_path)
        parser.error(f"Config file does not exist: {config_path}")

    if not config_path.is_file():
        logger.error("Config path is not a file: %s", config_path)
        parser.error(f"Config path is not a file: {config_path}")

    hash = file_hash_sha256(config_path).hexdigest()
    logger.info(f"Loading config from \"{config_path}\" sha256:{hash}")

    logger.debug("Calling configure(%s)", config_path)
    configure(config_path)
    logger.info("configure(%s) completed successfully", config_path)

    if MEDIATEST_ROOTDIR:
        rootdir = Path(MEDIATEST_ROOTDIR)
        logger.debug("Resolved mediatest_rootdir from config path: %s", rootdir)
    else:
        rootdir = config_path.resolve().parent
        logger.debug("No config path provided for mediatest_rootdir, defaulting to: %s", rootdir)
    
    logger.debug("mediatest_rootdir exists = %s", rootdir.exists())
    logger.debug("mediatest_rootdir is_dir = %s", rootdir.is_dir())

    test_path = rootdir / "tests" / "mediatests"
    logger.debug("Computed test_path=%s", test_path)
    logger.debug("test_path exists = %s", test_path.exists())
    logger.debug("test_path is_dir = %s", test_path.is_dir())

    pytest_args = [str(test_path), "--rootdir", str(rootdir)]
    logger.info("Executing pytest with args: %s", pytest_args)
    result = pytest.main(pytest_args)
    logger.info("pytest.main() returned %s", result)
    logger.debug("main() exiting with result=%s", result)
    return result
