from datetime import datetime, timedelta
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

# Allow Airflow to find our ETL modules
sys.path.append("/opt/airflow/project/src")

from extract import extract_data
from validate import validate_data
from load import load_to_staging
from transform import incremental_load


default_args = {
    "owner": "chandana",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="customer_etl_pipeline",
    default_args=default_args,
    description="Customer ETL pipeline using Python, PostgreSQL and Airflow",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "postgresql", "data-engineering"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
    )

    load_task = PythonOperator(
        task_id="load_to_staging",
        python_callable=load_to_staging,
    )

    transform_task = PythonOperator(
        task_id="incremental_load",
        python_callable=incremental_load,
    )

    extract_task >> validate_task >> load_task >> transform_task