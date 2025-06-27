{{ config(materialized='table') }}

SELECT
    customer_id,
    customer_name,
    customer_email,
    customer_region
FROM {{ ref('stg_dim_customer') }}
