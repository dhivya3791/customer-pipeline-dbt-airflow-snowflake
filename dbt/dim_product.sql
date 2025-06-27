{{ config(materialized='table') }}

SELECT
    product_id,
    product_name,
    product_category,
    unit_price
FROM {{ ref('stg_dim_product') }}
