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
  

## 🧭 Unified Data Flow into Snowflake

This project supports a **hybrid data ingestion strategy** by combining **cloud-native ingestion tools** with the existing **Airflow + dbt + Snowflake** pipeline.

---

### 1️⃣ Real-Time Clickstream Data

| Stage  | Tool                                             | Purpose                         |
|--------|--------------------------------------------------|---------------------------------|
| Capture | AWS Kinesis / Azure Event Hub                   | Ingest streaming user activity |
| Store   | AWS S3 / Azure Data Lake / OCI Object Storage   | Durable, scalable, cheap storage |
| Load    | Snowpipe or AWS Glue Streaming                  | Near real-time load into Snowflake |

---

### 2️⃣ Batch Data from Legacy Systems

| Stage    | Tool                                                       | Purpose                                |
|----------|------------------------------------------------------------|----------------------------------------|
| Export   | Custom scripts / Oracle Extract                            | Dump transactional data                |
| Land     | AWS S3 / Azure Data Lake / OCI Object Storage              | Cloud staging layer                    |
| Transform & Load | AWS Glue / Azure Data Factory / Oracle Data Integration | Clean, map, and load into Snowflake |

---

### 3️⃣ Post-Ingestion Processing (Your Existing Pipeline)

Once data lands in Snowflake, your existing Airflow pipeline takes over:

- 🧱 **dbt** transforms raw data into dimensional models (fact/dim tables)
- 🕹 **Airflow DAG** orchestrates dbt, applies **data quality checks**
- 📥 Any invalid rows are logged into the **`DATA_QUALITY_ISSUES`** table in Snowflake
- based on the issue to take decision to keep the record or not

---

## ✅ Tool Comparison by Key Needs

| Tool                             | Data Freshness              | Scalability            | Cost-Effectiveness                    |
|----------------------------------|-----------------------------|------------------------|----------------------------------------|
| AWS S3 + Glue                    | High (Snowpipe/streaming)   | Auto-scales            | Pay-per-use, cheap, highly reliable    |
| Azure Data Lake + Data Factory   | Moderate to high            | Azure-native scaling   | Good for Microsoft stack users         |
| Oracle OCI + Data Integration    | Good for Oracle systems     | High (with Data Flow)  | Efficient for on-prem Oracle migration |
| Airflow + dbt (existing)         | Flexible (scheduled/triggered) | Scales with cluster | Free/open source, modular, flexible    |

---

## 🔄 End-to-End Flow Summary
Web Clicks / Orders / CRM Data]
↓
[Cloud-native ingestion tools (Kinesis / Glue / Data Factory)]
↓
[Cloud Storage Layer (S3 / Azure Data Lake / OCI)]
↓
[Snowflake Raw Tables (via Snowpipe / ETL tools)]
↓
[dbt Models for transformation]
↓
[Data Quality Checks (Python + Airflow)]
↓
[Final Reporting Tables + Logged Issues]

| Tool                           | Purpose                                                                                                                                                        | Value                                                                          |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **ChatGPT** (GPT-4)            | - DAG debugging<br>- dbt integration help<br>- Data quality logic (e.g., referential checks, IQR) <br> -  Conceptual design help | Fast explanations, code examples, cleaned up vague errors, wrote documentation |





