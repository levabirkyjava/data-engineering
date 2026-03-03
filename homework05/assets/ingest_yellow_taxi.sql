/* @bruin

name: raw.yellow_taxi_trips
type: duckdb.sql

materialization:
  type: table
  strategy: time_interval
  time_column: pickup_datetime

columns:
  - name: pickup_datetime
    checks:
      - name: not_null
  - name: passenger_count
    checks:
      - name: positive
  - name: trip_distance
    checks:
      - name: positive

@bruin */

SELECT
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount
FROM read_parquet(
    'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{{ start_date[:7] }}.parquet'
)
WHERE pickup_datetime BETWEEN '{{ start_date }}' AND '{{ end_date }}'
