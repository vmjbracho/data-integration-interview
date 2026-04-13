import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Loads environment variables from a .env file and exposes them as attributes.

    Usage::

        from vmetrix.config import get_config
        config = get_config()
        print(config.TOKEN_BANXICO)
    """

    def __init__(self, env_path: str | Path | None = None) -> None:
        if env_path is None:
            env_path = Path(__file__).parent / ".env"

        self._path = Path(env_path)
        self._values: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.is_file():
            raise FileNotFoundError(f"No .env file found at {self._path}")

        with open(self._path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                self._values[key] = value
                os.environ.setdefault(key, value)

        logger.debug("Loaded %d variables from %s", len(self._values), self._path)

    def __getattr__(self, name: str) -> str:
        try:
            return self._values[name]
        except KeyError:
            raise AttributeError(f"Config has no variable '{name}'") from None

    def get(self, key: str, default: str | None = None) -> str | None:
        """Return a variable by name, or *default* if not present."""
        return self._values.get(key, default)


_config: Config | None = None


def get_config(env_path: str | Path | None = None) -> Config:
    """Return a singleton Config instance.

    The *env_path* argument is honored only on the first call; subsequent
    calls return the already-loaded singleton and log a warning if a
    different path is requested.
    """
    global _config
    if _config is None:
        _config = Config(env_path)
    elif env_path is not None and Path(env_path) != _config._path:
        logger.warning(
            "get_config() called with %s but singleton already loaded from %s",
            env_path, _config._path,
        )
    return _config
