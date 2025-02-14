from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
import pandas as pd


def extract_data(url, temp_file, **context):
    """
    Extract data from a URL and save it as a JSON file.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    with open(temp_file, 'w') as f:
        json.dump(data, f)


def transform_data(temp_file, temp_file_agg, **context):
    """
    Extracting only neccesery columns, transforming datatypes, adding columns
    """
    df = pd.DataFrame(temp_file)
    df = df[['date_utc', 'success', 'rocket', 'launchpad']]
    df['date_utc'] = pd.to_datetime(df['date_utc'])
    df['year'] = df['date_utc'].dt.year
    df['month'] = df['date_utc'].dt.month
    df['hour'] = df['date_utc'].dt.hour
    df.reset_index().to_csv(temp_file_agg) 
    

def load_data(temp_file_agg, **context):
    """
    Loading data into Postgres Database
    """
    engine = create_engine('postgresql+psycopg2://airflow:airflow@localhost:5432/spacex_db')
    temp_file_agg.to_sql('test_table', con=engine, if_exists='append', index=False)


dag = DAG(
    dag_id='dag',
    default_args={'owner': 'airflow'},
    schedule_interval='@monthly',
    start_date=days_ago(1)
)


extract_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    op_kwargs={
            'url': 'https://api.spacexdata.com/v4/launches',
            'tmp_file': '/tmp/file.csv'
    },
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    op_kwargs={
            'tmp_file': '/tmp/file.csv',
            'tmp_agg_file': '/tmp/file_agg.csv'
    },
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    op_kwargs={
            'tmp_agg_file': '/tmp/file_agg.csv'
    },
    dag=dag,
)


extract_task >> transform_task >> load_task
