from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys
import os
import pandas as pd

sys.path.insert(0, '/opt/airflow/src')

from extract_data import extract_data
from transform_data import data_transformations
from load_data import load_data_to_database, engine
from dotenv import load_dotenv   

path_env = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(path_env)

api_key = os.getenv("API_KEY")

url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={api_key}'


@dag(
    dag_id="dag_weather",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    description = 'Pipeline ETL - Clima Sao Paulo',
    start_date = datetime(2026, 9, 14),
    schedule = '0 */1 * * *',
    catchup = False,
    tags = ["WEATHER", "ETL"]
)


def weather_pipeline():

    @task
    def extract():
        extract_data(url)
        
    @task
    def transform():
        df = data_transformations()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)
        
    @task 
    def load():
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_data_to_database(df, 'sp_weather', engine)
        
    extract() >> transform() >> load()

weather_pipeline()