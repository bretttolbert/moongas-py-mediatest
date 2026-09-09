import argparse
import logging
import sys
from pathlib import Path

import pytest

from mediatest.config import configure

logger = logging.getLogger(__name__)


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

    logger.debug("Calling configure(%s)", config_path)
    configure(config_path)
    logger.info("configure(%s) completed successfully", config_path)

    test_root = config_path.resolve().parent
    logger.debug("Resolved test_root from config file path: %s", test_root)
    logger.debug("test_root exists = %s", test_root.exists())
    logger.debug("test_root is_dir = %s", test_root.is_dir())

    test_path = test_root / "tests" / "mediatests"
    logger.debug("Computed test_path=%s", test_path)
    logger.debug("test_path exists = %s", test_path.exists())
    logger.debug("test_path is_dir = %s", test_path.is_dir())

    pytest_args = [str(test_path), "--rootdir", str(test_root)]
    logger.info("Executing pytest with args: %s", pytest_args)
    result = pytest.main(pytest_args)
    logger.info("pytest.main() returned %s", result)
    logger.debug("main() exiting with result=%s", result)
    return result
