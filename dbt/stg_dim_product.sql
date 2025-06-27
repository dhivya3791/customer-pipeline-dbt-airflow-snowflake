{{ config(materialized='view') }}

SELECT
    CAST(product_id AS INT) AS product_id,
    INITCAP(TRIM(product_name)) AS product_name,
    INITCAP(TRIM(product_category)) AS product_category,
    CAST(unit_price AS FLOAT) AS unit_price
FROM {{ source('raw', 'dim_product') }}
WHERE product_id IS NOT NULL
