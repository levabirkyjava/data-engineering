from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator

PROJECT_ID = "{{ var.value.gcp_project_id }}"
RAW_DATASET = "{{ var.value.raw_dataset }}"
LAKE_BUCKET = "{{ var.value.lake_bucket }}"
SOURCE_TABLE = os.getenv(
    "SOURCE_TABLE",
    "bigquery-public-data.chicago_taxi_trips.taxi_trips",
)

DEFAULT_ARGS = {
    "owner": "course-project",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="chicago_taxi_batch_pipeline",
    default_args=DEFAULT_ARGS,
    description="Batch pipeline: BigQuery public data -> raw BQ -> GCS parquet -> dbt marts",
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["chicago", "taxi", "batch"],
) as dag:
    create_raw_table = BigQueryInsertJobOperator(
        task_id="create_raw_table",
        configuration={
            "query": {
                "query": f"""
                CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{RAW_DATASET}.chicago_taxi_trips` (
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
                """,
                "useLegacySql": False,
            }
        },
    )

    ingest_increment = BigQueryInsertJobOperator(
        task_id="ingest_increment",
        configuration={
            "query": {
                "query": f"""
                INSERT INTO `{PROJECT_ID}.{RAW_DATASET}.chicago_taxi_trips`
                SELECT
                  CAST(taxi_id AS STRING) AS trip_id,
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
                FROM `{SOURCE_TABLE}`
                WHERE DATE(trip_start_timestamp) = DATE('{{{{ ds }}}}')
                """,
                "useLegacySql": False,
            }
        },
    )

    export_raw_partition = BigQueryToGCSOperator(
        task_id="export_raw_partition",
        source_project_dataset_table=f"{PROJECT_ID}:{RAW_DATASET}.chicago_taxi_trips${{{{ ds_nodash }}}}",
        destination_cloud_storage_uris=[
            f"gs://{LAKE_BUCKET}/raw/chicago_taxi_trips/date={{{{ ds }}}}/part-*.parquet"
        ],
        export_format="PARQUET",
        print_header=False,
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dbt && dbt build --profiles-dir /opt/airflow/dbt --target prod",
    )

    create_raw_table >> ingest_increment >> export_raw_partition >> run_dbt

