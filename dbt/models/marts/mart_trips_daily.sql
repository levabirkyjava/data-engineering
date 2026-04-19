{{ config(
    partition_by={"field": "trip_date", "data_type": "date"}
) }}

select
  trip_date,
  count(*) as trips_cnt,
  avg(trip_miles) as avg_trip_miles,
  avg(trip_total) as avg_trip_total,
  sum(trip_total) as revenue_total
from {{ ref('stg_chicago_taxi_trips') }}
group by trip_date

