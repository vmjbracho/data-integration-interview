# config.py

from datetime import date
_today = date.today().strftime("%Y-%m-%d")

# Scope de activos definidos para el proyecto
SECURITY_LIST = [
    "USDMXN.FIX",
    "UDIMXN.SPOT",
    "MXN.TPFB",
    "MXN.TIIE-1D"
]

# Versión formateada para queries SQL (IN ('...', '...'))
SECURITY_LIST_STR = ", ".join(f"'{sec}'" for sec in SECURITY_LIST)

# Rutas de almacenamiento

PATH_RAW      = 's3_datalake/historical/raw'
PATH_INC      = 's3_datalake/incremental/raw'
PATH_REPORT   = 'report'