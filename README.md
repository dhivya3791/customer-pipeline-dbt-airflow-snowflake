# customer-pipeline-dbt-powerbi-airflow
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

- **dbt-core 1.10**
- **Snowflake Cloud Data Platform**
- **Anaconda (Python 3.10 environment)**
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

## ▶️ How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/customer-pipeline-dbt.git
   cd customer-pipeline-dbt
