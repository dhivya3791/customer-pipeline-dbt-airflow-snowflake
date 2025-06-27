{{ config(materialized='view') }}

SELECT
    CAST(date_id AS DATE) AS date_id,
    INITCAP(day_of_week) AS day_of_week,
    INITCAP(month_name) AS month_name,
    CAST(quarter AS INT) AS quarter,
    CAST(year AS INT) AS year
FROM {{ source('raw', 'dim_date') }}
WHERE date_id IS NOT NULL
