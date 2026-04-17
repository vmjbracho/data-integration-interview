/*
* LocalDb schema
*/

/*
CREATE TABLE BANXICO_SERIES(
  SECURITY_NAME VARCHAR,
  IDSERIE VARCHAR,
  TITULO VARCHAR,
  PERIODICIDAD VARCHAR,
  CIFRA VARCHAR,
  UNIDAD VARCHAR
);
*/

CREATE TABLE IF NOT EXISTS fact_securities (
    date DATE,
    series_id VARCHAR,
    security_name VARCHAR,
    value DOUBLE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (date, series_id)
);

CREATE OR REPLACE VIEW v_securities_stats AS
SELECT
    security_name,
    series_id,
    date,
    value,
    MIN(value) OVER w AS min_7d,
    MAX(value) OVER w AS max_7d,
    AVG(value) OVER w AS avg_7d
FROM fact_securities
WINDOW w AS (
    PARTITION BY series_id
    ORDER BY date
    RANGE BETWEEN INTERVAL 6 DAYS PRECEDING AND CURRENT ROW
);