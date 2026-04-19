{{ config(
    unique_key='trip_id',
    partition_by={"field": "trip_date", "data_type": "date"},
    cluster_by=["payment_type", "company"]
) }}

with src as (
    select
        cast(trip_id as string) as trip_id,
        timestamp(trip_start_timestamp) as trip_start_timestamp,
        timestamp(trip_end_timestamp) as trip_end_timestamp,
        date(trip_start_timestamp) as trip_date,
        cast(trip_seconds as int64) as trip_seconds,
        cast(trip_miles as numeric) as trip_miles,
        cast(fare as numeric) as fare,
        cast(tips as numeric) as tips,
        cast(tolls as numeric) as tolls,
        cast(extras as numeric) as extras,
        cast(trip_total as numeric) as trip_total,
        coalesce(nullif(cast(payment_type as string), ''), 'Unknown') as payment_type,
        coalesce(nullif(cast(company as string), ''), 'Unknown') as company
    from `{{ env_var('DBT_BIGQUERY_PROJECT') }}.{{ env_var('RAW_DATASET', 'raw') }}.chicago_taxi_trips`
    where trip_start_timestamp is not null
)

select *
from src

{% if is_incremental() %}
where trip_date >= date_sub(current_date(), interval 7 day)
{% endif %}

