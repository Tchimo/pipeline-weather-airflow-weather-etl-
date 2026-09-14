import requests
import json
from pathlib import Path 
import logging
#import os
#from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#env_path = '../config/.env'

#load_dotenv(env_path)
#api_key = os.getenv("API_KEY")
#city = "Sao Paulo"
#unit = "metric"

#url = f'https://api.openweathermap.org/data/2.5/weather?q={city},BR&units={unit}&appid={api_key}'

def extract_data(url: str) -> dict:
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        logging.error(f"Erro na requisição para {url}: {e}")
        return {}

    if response.status_code != 200:
        logging.error(f"Falha ao buscar dados de {url}. Status code: {response.status_code}")
        return {}

    try:
        data = response.json()
    except ValueError:
        logging.error("Resposta da API não é um JSON válido")
        return {}

    if not data:
        logging.warning(f"Nenhum dado retornado de {url}")
        return {}

    output_path = "/opt/airflow/data/weather_data.json"
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"Dados extraídos com sucesso e salvos em {output_path}")

    return data


#if __name__ == "__main__":
 #   extract_data(url)