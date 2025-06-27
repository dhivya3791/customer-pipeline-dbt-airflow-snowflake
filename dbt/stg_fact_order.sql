{{ config(materialized='view') }}

SELECT
    CAST(order_id AS INT) AS order_id,
    CAST(customer_id AS INT) AS customer_id,
    CAST(product_id AS INT) AS product_id,
    CAST(date_id AS DATE) AS date_id,
    COALESCE(CAST(quantity AS INT), 0) AS quantity,
    COALESCE(CAST(total_amount AS FLOAT), 0.0) AS total_amount
FROM {{ source('raw', 'fact_order') }}
WHERE order_id IS NOT NULL
