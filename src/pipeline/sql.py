from __future__ import annotations

from datetime import date

from pipeline.config import PipelineConfig


def raw_table_fqn(cfg: PipelineConfig) -> str:
    return f"`{cfg.project_id}.{cfg.raw_dataset}.chicago_taxi_trips`"


def build_create_raw_table_sql(cfg: PipelineConfig) -> str:
    table = raw_table_fqn(cfg)
    return f"""
CREATE TABLE IF NOT EXISTS {table} (
  trip_id STRING,
  trip_start_timestamp TIMESTAMP,
  trip_end_timestamp TIMESTAMP,
  trip_seconds INT64,
  trip_miles NUMERIC,
  fare NUMERIC,
  tips NUMERIC,
  tolls NUMERIC,
  extras NUMERIC,
  trip_total NUMERIC,
  payment_type STRING,
  company STRING
)
PARTITION BY DATE(trip_start_timestamp)
CLUSTER BY payment_type, company
""".strip()


def build_incremental_insert_sql(cfg: PipelineConfig, run_date: date) -> str:
    table = raw_table_fqn(cfg)
    run_date_iso = run_date.isoformat()
    return f"""
INSERT INTO {table}
SELECT
  CAST(trip_id AS STRING) AS trip_id,
  trip_start_timestamp,
  trip_end_timestamp,
  CAST(trip_seconds AS INT64) AS trip_seconds,
  CAST(trip_miles AS NUMERIC) AS trip_miles,
  CAST(fare AS NUMERIC) AS fare,
  CAST(tips AS NUMERIC) AS tips,
  CAST(tolls AS NUMERIC) AS tolls,
  CAST(extras AS NUMERIC) AS extras,
  CAST(trip_total AS NUMERIC) AS trip_total,
  CAST(payment_type AS STRING) AS payment_type,
  CAST(company AS STRING) AS company
FROM `{cfg.source_table}`
WHERE DATE(trip_start_timestamp) = DATE('{run_date_iso}')
""".strip()


def build_tile_queries(cfg: PipelineConfig) -> dict[str, str]:
    analytics = f"`{cfg.project_id}.{cfg.analytics_dataset}`"
    return {
        "categorical_payment_distribution": f"""
SELECT payment_type, SUM(trips_cnt) AS trips_cnt
FROM {analytics}.mart_payment_type_daily
GROUP BY payment_type
ORDER BY trips_cnt DESC
""".strip(),
        "temporal_daily_trend": f"""
SELECT trip_date, trips_cnt
FROM {analytics}.mart_trips_daily
ORDER BY trip_date
""".strip(),
    }

