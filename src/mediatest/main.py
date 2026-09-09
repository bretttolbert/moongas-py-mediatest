import argparse
import logging
from pathlib import Path

import pytest

from mediatest.config import configure

logger = logging.getLogger(__name__)


def main(config_path: Path | None = None) -> int:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger.debug("main() starting with config_path=%r", config_path)

    if config_path is None:
        logger.debug("No config_path provided; parsing CLI arguments.")
        parser = argparse.ArgumentParser()
        parser.add_argument("config_path", type=Path, nargs="?")
        parsed_args = parser.parse_args()
        logger.debug("Parsed CLI args: %s", parsed_args)
        config_path = parsed_args.config_path
        logger.info("Using CLI config_path=%r", config_path)
    else:
        logger.info("Using provided config_path=%r", config_path)

    logger.debug("Calling configure(%r)", config_path)
    configure(config_path)
    logger.info("configure(%r) completed successfully", config_path)

    if config_path is not None:
        test_root = config_path.resolve().parent
        logger.debug("Resolved test_root from config file path: %s", test_root)
    else:
        test_root = Path(__file__).resolve().parents[2]
        logger.warning(
            "config_path was None; falling back to project root derived from __file__: %s",
            test_root,
        )

    test_path = test_root / "tests" / "mediatests"
    logger.debug("Computed test_path=%s", test_path)

    pytest_args = [str(test_path), "--rootdir", str(test_root)]
    logger.info("Executing pytest with args: %s", pytest_args)
    result = pytest.main(pytest_args)
    logger.info("pytest.main() returned %s", result)
    logger.debug("main() exiting with result=%s", result)
    return result
