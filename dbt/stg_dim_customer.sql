{{ config(materialized='view') }}

SELECT
    CAST(customer_id AS INT) AS customer_id,
    LOWER(TRIM(customer_name)) AS customer_name,
    LOWER(TRIM(customer_email)) AS customer_email,
    INITCAP(TRIM(customer_region)) AS customer_region
FROM {{ source('raw', 'dim_customer') }}
WHERE customer_id IS NOT NULL
