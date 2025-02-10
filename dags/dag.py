from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.extract import fetch_data
from src.transform import clean_data
from src.load import load_to_db
import yaml
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)


def extract_data(**kwargs):
    try:
        config = load_config()
        api_url = config["api"]["url"]
        data = fetch_data(api_url)
        kwargs["ti"].xcom_push(key="data", value=data)
    except Exception as e:
        logging.error(f"Error extracting data: {str(e)}")
        raise


def transform_data(**kwargs):
    try:
        ti = kwargs["ti"]
        raw_data = ti.xcom_pull(key="data")
        df = clean_data(raw_data)
        kwargs["ti"].xcom_push(key="df", value=df.to_dict(orient="records"))
    except Exception as e:
        logging.error(f"Error transforming data: {str(e)}")
        raise


def load_data(**kwargs):
    try:
        config = load_config()
        ti = kwargs["ti"]
        df_records = ti.xcom_pull(key="df")
        df = pd.DataFrame.from_records(df_records)
        db_connection = f"postgresql+psycopg2://{config['database']['user']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['dbname']}"
        load_to_db(df, db_connection, config["database"]["table_name"])
    except Exception as e:
        logging.error(f"Error loading data to DB: {str(e)}")
        raise


default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 2, 10),
}


dag = DAG(
    "spacex_etl",
    default_args=default_args,
    description="ETL pipeline for SpaceX launches data",
    schedule_interval=timedelta(days=7),
    catchup=False,
)


extract_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    dag=dag,
)


extract_task >> transform_task >> load_task
