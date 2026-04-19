{{ config(
    partition_by={"field": "trip_date", "data_type": "date"},
    cluster_by=["payment_type"]
) }}

select
  trip_date,
  payment_type,
  count(*) as trips_cnt,
  sum(trip_total) as revenue_total
from {{ ref('stg_chicago_taxi_trips') }}
group by trip_date, payment_type

