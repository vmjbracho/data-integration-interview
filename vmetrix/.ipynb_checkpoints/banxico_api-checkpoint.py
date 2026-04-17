import logging
from typing import Any

import httpx

from vmetrix.config import get_config

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 15.0
DEFAULT_RETRIES = 3


class BanxicoAPI:
    """Client for the Banxico SIE REST API.

    Provides methods to query economic series metadata and data points
    from the Sistema de Informacion Economica (SIE) of Banco de Mexico.

    Uses a persistent ``httpx.Client`` so TCP/TLS connections are reused
    across calls. Safe to use as a context manager; otherwise call
    :meth:`close` when done.
    """

    BASE_URL = "https://www.banxico.org.mx/SieAPIRest/service"

    def __init__(
        self,
        token: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
    ):
        self._token = token or get_config().get("TOKEN_BANXICO")
        if not self._token:
            raise ValueError(
                "TOKEN_BANXICO is not set — add it to vmetrix/.env or pass token=..."
            )

        self._client = httpx.Client(
            base_url=self.BASE_URL,
            headers={"Bmx-Token": self._token},
            timeout=timeout,
            transport=httpx.HTTPTransport(retries=retries),
        )

    def __repr__(self) -> str:
        return f"BanxicoAPI(base_url={self.BASE_URL})"

    def __enter__(self) -> "BanxicoAPI":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _get(self, endpoint: str, raw_response: bool = False) -> Any:
        path = "/" + endpoint.lstrip("/")
        logger.debug("GET %s%s", self.BASE_URL, path)

        response = self._client.get(path)
        response.raise_for_status()

        logger.info(
            f"GET {self.BASE_URL + path} -> HTTP: {response.status_code}",
        )

        if raw_response:
            return f"{response.status_code}: {response.text}"
        return response.json()

    def get_metadata(self, series: str, raw_response: bool = False) -> Any:
        """Retrieve metadata for the given series (comma-separated IDs)."""
        return self._get(f"v1/series/{series}", raw_response=raw_response)

    def get_last_value(self, series: str, raw_response: bool = False) -> Any:
        """Retrieve the most recent data point for the given series."""
        return self._get(
            f"v1/series/{series}/datos/oportuno", raw_response=raw_response
        )

    def get_values_between(
        self,
        series: str,
        start_date: str,
        end_date: str,
        raw_response: bool = False,
    ) -> Any:
        """Retrieve data points for the given series within ``[start, end]``.

        Dates must be in ``YYYY-MM-DD`` format.
        """
        return self._get(
            f"v1/series/{series}/datos/{start_date}/{end_date}",
            raw_response=raw_response,
        )


def get_banxico_api() -> BanxicoAPI:
    """Create and return a new BanxicoAPI instance."""
    return BanxicoAPI()
