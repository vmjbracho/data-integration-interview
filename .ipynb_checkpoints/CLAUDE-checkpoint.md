# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo is a **technical-interview exercise** for a Data Integration Engineer role. The candidate must build a productive ETL pipeline that:

1. Consumes the Banxico SIE REST API.
2. Transforms data with **DuckDB** (or Python — choice must be justified per case).
3. Persists *RAW* responses into [s3_datalake/](s3_datalake/) (simulated S3 datalake) as Parquet.
4. Loads curated data back into the local DuckDB file.
5. Provides observability (logging) at every layer and is re-runnable (idempotent).

The brief lives in [interview.ipynb](interview.ipynb); sample API/DB calls are in [code_examples.ipynb](code_examples.ipynb); the business-case diagram is [img/business_case.png](img/business_case.png).

## Architecture

The `vmetrix` package provides three singletons used everywhere via the top-level imports in [vmetrix/__init__.py](vmetrix/__init__.py):

- `get_config()` → [vmetrix/config.py](vmetrix/config.py): tiny hand-rolled `.env` loader (no `python-dotenv`). Reads `vmetrix/.env` by default and caches a process-wide singleton. `TOKEN_BANXICO` is the main secret consumed.
- `get_database()` → [vmetrix/database.py](vmetrix/database.py): `LocalDb` wrapper around a file-backed DuckDB at `vmetrix/db.duckdb`. **Each call opens and closes its own connection** on purpose — this avoids Windows file-lock errors when notebook cells or separate processes touch the DB concurrently. `query()` displays a DataFrame (notebook-oriented, uses `IPython.display`); `command()` runs DDL/DML without returning rows.
- `get_banxico_api()` → [vmetrix/banxico_api.py](vmetrix/banxico_api.py): `httpx`-based client for `https://www.banxico.org.mx/SieAPIRest/service`. Three endpoints: `get_metadata`, `get_last_value` (`/datos/oportuno`), `get_values_between` (`/datos/{start}/{end}`). All accept comma-separated series IDs and a `raw_response` flag.

The only pre-existing table is `BANXICO_SERIES` (see [vmetrix/database.sql](vmetrix/database.sql)) which maps human-readable `SECURITY_NAME` (e.g. `USDMXN.FIX`) to Banxico `IDSERIE` (e.g. `SF43718`). **Security names are the contract with the candidate's code; series IDs are looked up from this table.**

## Task requirements (from [interview.ipynb](interview.ipynb))

Target securities: `USDMXN.FIX`, `UDIMXN.SPOT`, `MXN.TPFB`, `MXN.TIIE-1D`.

1. **Historical load** from `2025-01-01` to today into a new DuckDB table; document schema in `vmetrix/database.sql`.
2. **Daily incremental load** of current-day values.
3. **7-day rolling stats table** (min / max / avg) per security.
4. `UDIMXN.SPOT` special case: updates only on the 10th and 25th of each month — persist the latest available date, do not assume daily values.
5. Store raw API responses under [s3_datalake/](s3_datalake/) for reprocessing/debug (candidate designs the partitioning).
6. Pipeline must be **re-runnable**: a second execution deletes prior records for the same window before inserting.
7. Add `logging` at each stage; justify DuckDB-vs-Python for each transform.

## Conventions worth knowing

- Banxico API returns dates as `DD/MM/YYYY` strings and values as strings — conversion happens in candidate code, not in the client.
- `.env` is committed at [vmetrix/.env](vmetrix/.env) (interview-only token).
- `config.py` calls `os.environ.setdefault`, so loaded vars become process env but won't overwrite anything already set.
- No build / lint / test tooling is configured — work is driven from the notebooks. Run cells in [code_examples.ipynb](code_examples.ipynb) to sanity-check API/DB access before editing candidate solution code.
- Paths inside `vmetrix` are resolved relative to `__file__`, so the DB and `.env` always sit next to the package regardless of CWD.
