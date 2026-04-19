from datetime import date

from pipeline.config import PipelineConfig
from pipeline.sql import (
    build_create_raw_table_sql,
    build_incremental_insert_sql,
    build_tile_queries,
)


def _cfg() -> PipelineConfig:
    return PipelineConfig(project_id="demo-project")


def test_create_raw_table_contains_partition_and_cluster() -> None:
    sql = build_create_raw_table_sql(_cfg())
    assert "PARTITION BY DATE(trip_start_timestamp)" in sql
    assert "CLUSTER BY payment_type, company" in sql


def test_incremental_insert_contains_date_filter() -> None:
    sql = build_incremental_insert_sql(_cfg(), date(2024, 2, 20))
    assert "DATE('2024-02-20')" in sql
    assert "bigquery-public-data.chicago_taxi_trips.taxi_trips" in sql


def test_tile_queries_have_both_required_tiles() -> None:
    queries = build_tile_queries(_cfg())
    assert "categorical_payment_distribution" in queries
    assert "temporal_daily_trend" in queries

