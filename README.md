# customer-pipeline-dbt-airflow
End-to-end dbt project using Snowflake
# Customer Pipeline – dbt Project (Snowflake)

This is a complete end-to-end data pipeline built using **dbt** (Data Build Tool) and **Snowflake** as the data warehouse. It demonstrates how to clean, model, test, and document data using best practices in modern data engineering.

---

## 🏗️ Project Overview

This project builds a star schema around customer orders, including:

- `dim_customer`: Customer details (name, email, region)
- `dim_product`: Product info (name, category, unit price)
- `dim_date`: Calendar attributes (day, month, year)
- `fact_orders`: Order data joined with all dimensions

---

## 🔧 Tools & Tech

- **dbt (Data Build Tool)** for transformations
- **Snowflake** as the cloud data warehouse
- **Python (with Pandas)** for custom data quality checks
- **Apache Airflow** for orchestration 
- Git & GitHub

---

## 🗃️ Data Flow (Snowflake)

1. **Raw Tables** (in Snowflake):
   - `dim_customer`, `dim_product`, `dim_date`, `fact_order`

2. **Staging Layer (`stg_`)**:
   - Cleaned views using dbt models
   - Basic transformations: trimming, lowercasing, null handling

3. **Final Models (`dim_`, `fact_`)**:
   - Materialized as tables
   - Joined to form a proper star schema

---

## ✅ dbt Features Used

- `ref()` and `source()` for dependency tracking
- Model materializations: `view` for staging, `table` for final
- Tests:
  - `not_null`, `unique`
  - `relationships` (foreign keys)
- `schema.yml` documentation for all models

---
## 🔧 Key Features

- 🔄 Runs on Docker using `docker-compose`
- ✅ Builds dimension and fact tables with `dbt`
- 🔍 Performs **data quality checks**:
  - **Referential Integrity Checks** (e.g., `customer_id` & `product_id`)
  - **IQR-based Outlier Detection**
- 🧾 **Logs invalid/missing rows into Snowflake** for review
- 📊 Modular design for extensibility

## ⚙️ Workflow Overview
### 1. **dbt Transformation**
Airflow runs `dbt run` to build models:
- `DIM_CUSTOMER`
- `DIM_PRODUCT`
- `FACT_ORDERS`
### 2. **Data Quality Checks**
`PythonOperator` executes:
- **Referential Integrity Check**
  - Ensures `customer_id` in `FACT_ORDERS` exists in `DIM_CUSTOMER`
  - Ensures `product_id` in `FACT_ORDERS` exists in `DIM_PRODUCT`
- **IQR (Interquartile Range) Check**
  - Detects outliers in numerical fields (e.g., `order_amount`)
  - Rows outside of 1.5 * IQR bounds are flagged

### 3. **Issue Logging**
- Any rows failing integrity or IQR checks are written to a Snowflake table:
  - `DATA_QUALITY_ISSUES`




