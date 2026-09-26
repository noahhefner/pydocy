import logging
from logging import getLogger
from pathlib import Path

from pydocy.walk_source import walk_source

logger: logging.Logger = getLogger(__name__)


def test_tree():

    path = Path(__file__) / "how-tui" / "src"

    results = walk_source(path)

    logger.info(results)

    assert results is not None
