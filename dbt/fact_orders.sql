{{ config(materialized='table') }}

SELECT
    f.order_id,
    f.date_id,
    d.day_of_week,
    d.month_name,
    d.quarter,
    d.year,
    f.customer_id,
    c.customer_name,
    c.customer_email,
    c.customer_region,
    f.product_id,
    p.product_name,
    p.product_category,
    p.unit_price,
    f.quantity,
    f.total_amount
FROM {{ ref('stg_fact_order') }} AS f
LEFT JOIN {{ ref('dim_date') }} AS d ON f.date_id = d.date_id
LEFT JOIN {{ ref('dim_customer') }} AS c ON f.customer_id = c.customer_id
LEFT JOIN {{ ref('dim_product') }} AS p ON f.product_id = p.product_id
