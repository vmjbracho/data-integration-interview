import logging

from vmetrix.banxico_api import BanxicoAPI, get_banxico_api
from vmetrix.config import Config, get_config
from vmetrix.database import LocalDb, get_database

__all__ = [
    "BanxicoAPI",
    "Config",
    "LocalDb",
    "get_banxico_api",
    "get_config",
    "get_database",
]


def _configure_logging() -> None:
    """Attach a StreamHandler to the ``vmetrix`` logger at INFO level."""
    logger = logging.getLogger("vmetrix")
    if logger.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt=">>> %(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%d/%b/%Y %I:%M:%S %p",
        )
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


_configure_logging()
