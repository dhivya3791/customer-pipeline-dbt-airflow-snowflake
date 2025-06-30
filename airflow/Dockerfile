FROM apache/airflow:2.9.1

USER root

# Install system packages (as root)
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# Switch to airflow user for pip install (required!)
USER airflow

RUN pip install --no-cache-dir dbt-core dbt-snowflake
