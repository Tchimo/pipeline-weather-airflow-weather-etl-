from sqlalchemy import create_engine, text
import pandas as pd
from urllib.parse import quote_plus
import logging
import os
import pathlib
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

path = pathlib.Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(path)

database_name = os.getenv("DATABASE_NAME")
user_name = os.getenv("USER_NAME") 
password = os.getenv("PASSWORD")
host = "host.docker.internal"  # Use "host.docker.internal" for Docker on Windows and Mac, or "localhost" for Linux


def create_database_engine(database_name: str, user_name: str, password: str):
    connection_string = f"postgresql+psycopg2://{user_name}:{quote_plus(password)}@{host}:5432/{database_name}"
    engine = create_engine(connection_string)
    return engine

engine = create_database_engine(database_name, user_name, password)


def load_data_to_database(df: pd.DataFrame, table_name: str, engine):
    try:
        df.to_sql(
            name = table_name, 
            con = engine, 
            if_exists='append', 
            index=False)
        logging.info(f"✓ Dados carregados com sucesso na tabela '{table_name}' do banco de dados '{database_name}'")
    except Exception as e:
        logging.error(f"Erro ao carregar dados na tabela '{table_name}': {e}")

    df_check = pd.read_sql_query(text(f"SELECT * FROM {table_name} LIMIT 5"), engine)
    logging.info(f"\n✓ Verificação de dados carregados:\n{df_check}")

