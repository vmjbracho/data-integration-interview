import logging
from pathlib import Path
from typing import Any, Sequence

import duckdb
import pandas as pd

logger = logging.getLogger(__name__)


class LocalDb:
    """Local DuckDB database backed by a file stored alongside the package.

    Each method opens and closes its own connection, so the database file
    is never held locked between calls. This avoids "file in use" errors
    when multiple notebook cells or processes access the same file::

        db = get_database()
        df = db.query("SELECT * FROM BANXICO_SERIES")
        db.command("DELETE FROM my_table WHERE dt = ?", ["2026-01-01"])
        db.write_df("my_table", df, mode="replace")
    """

    def __init__(self, path: str | Path | None = None):
        self._path = Path(path) if path else Path(__file__).parent / "db.duckdb"

    def __repr__(self) -> str:
        return f"LocalDb(file_path={self._path.absolute()})"

    def query(
        self, sql: str, params: Sequence[Any] | None = None
    ) -> pd.DataFrame:
        """Execute a SELECT and return the result as a DataFrame."""
        logger.debug("query: %s | params=%s", sql, params)
        with duckdb.connect(self._path) as conn:
            rel = conn.execute(sql, params) if params else conn.execute(sql)
            return rel.df()

    def command(
        self, sql: str, params: Sequence[Any] | None = None
    ) -> None:
        """Execute a DDL/DML statement that does not return rows."""
        logger.debug("command: %s | params=%s", sql, params)
        with duckdb.connect(self._path) as conn:
            if params:
                conn.execute(sql, params)
            else:
                conn.execute(sql)

    def write_df(
        self, table: str, df: pd.DataFrame, mode: str = "append"
    ) -> int:
        """Persist a DataFrame into *table*.

        Args:
            table: destination table name.
            df: DataFrame to insert.
            mode: ``append`` (default), ``replace`` (drop + recreate), or
                ``create`` (CREATE TABLE AS — fails if table exists).

        Returns:
            Number of rows written.
        """
        if mode not in {"append", "replace", "create"}:
            raise ValueError(f"Invalid mode: {mode!r}")

        logger.info("write_df: table=%s mode=%s rows=%d", table, mode, len(df))
        with duckdb.connect(self._path) as conn:
            conn.register("_df", df)
            try:
                if mode == "replace":
                    conn.execute(f"DROP TABLE IF EXISTS {table}")
                    conn.execute(f"CREATE TABLE {table} AS SELECT * FROM _df")
                elif mode == "create":
                    conn.execute(f"CREATE TABLE {table} AS SELECT * FROM _df")
                else:
                    conn.execute(f"INSERT INTO {table} SELECT * FROM _df")
            finally:
                conn.unregister("_df")
        return len(df)


def get_database(path: str | Path | None = None) -> LocalDb:
    """Create and return a new LocalDb instance."""
    return LocalDb(path)
