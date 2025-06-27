{{ config(materialized='table') }}

SELECT
    date_id,
    day_of_week,
    month_name,
    quarter,
    year
FROM {{ ref('stg_dim_date') }}
