from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
import sys

# Add dags folder to path if needed to import data_quality.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_quality import run_data_quality_checks  # must match function name in data_quality.py

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='dbt_and_data_quality_pipeline',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['dbt', 'snowflake', 'data_quality'],
) as dag:

    # Step 1: Run dbt models
    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command=(
    "cd /opt/airflow/dbt_project && "
    "/home/airflow/.local/bin/dbt run --profiles-dir /opt/airflow/dbt_project/profiles"
),

        env={
            'SNOWFLAKE_PW': os.getenv('SNOWFLAKE_PW', ''),
        }
    )

    # Step 2: Run data quality checks using your python script
    data_quality_check = PythonOperator(
        task_id='run_data_quality_checks',
        python_callable=run_data_quality_checks
    )

    run_dbt >> data_quality_check
