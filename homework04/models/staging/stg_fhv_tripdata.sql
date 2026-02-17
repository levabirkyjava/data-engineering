{{ config(materialized='view') }}

SELECT
    dispatching_base_num,
    {{ dbt.safe_cast("pickup_datetime", api.Column.translate_type("timestamp")) }} as pickup_datetime,
    {{ dbt.safe_cast("dropoff_datetime", api.Column.translate_type("timestamp")) }} as dropoff_datetime,
    PUlocationID as pickup_location_id,
    DOlocationID as dropoff_location_id,
    SR_Flag as sr_flag,
    Affiliated_base_number as affiliated_base_number
FROM {{ source('staging', 'fhv_tripdata') }}
WHERE dispatching_base_num IS NOT NULL

{% if var('is_test_run', default=true) %}
  LIMIT 100
{% endif %}
