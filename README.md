# Pipeline Weather

Pipeline de ETL (Extract, Transform, Load) que coleta dados meteorológicos em tempo real da API [OpenWeatherMap](https://openweathermap.org/api), realiza transformações nos dados e os carrega em um banco de dados PostgreSQL. O pipeline pode ser orquestrado com **Apache Airflow** via Docker Compose.

## 🚀 Tecnologias

- **Python 3.13**
- **Pandas** — transformação e manipulação de dados
- **Requests** — extração de dados via API
- **SQLAlchemy** + **psycopg2** — conexão e carga no PostgreSQL
- **python-dotenv** — gerenciamento de variáveis de ambiente
- **uv** — gerenciamento de dependências e ambiente virtual
- **Apache Airflow 3.1.7** — orquestração do pipeline (via Docker Compose)
- **Docker Compose** — orquestração dos serviços (Postgres, Redis, Airflow)

## 📁 Estrutura do projeto

```
pipeline-weather/
├── src/
│   ├── extract_data.py       # Extração dos dados da API OpenWeatherMap
│   ├── transform_data.py     # Transformações no dataset
│   └── load_data.py          # Carga dos dados no PostgreSQL
├── config/
│   └── .env                  # Variáveis de ambiente (não versionado)
├── dags/                     # DAGs do Airflow
├── logs/                     # Logs do Airflow
├── plugins/                  # Plugins do Airflow
├── data/                     # Dados persistidos localmente
├── main.py                   # Ponto de entrada do pipeline
├── docker-compose.yaml       # Orquestração dos serviços com Airflow
├── pyproject.toml            # Dependências e metadados do projeto
└── uv.lock                   # Lockfile das dependências (uv)
```

## ⚙️ Como funciona o pipeline

O `main.py` executa três etapas sequenciais:

1. **Extract** — busca os dados climáticos atuais da cidade de São Paulo (BR) na API OpenWeatherMap.
2. **Transform** — aplica as transformações necessárias nos dados extraídos.
3. **Load** — carrega os dados tratados na tabela `sp_weather` do PostgreSQL.

## 🔧 Configuração

### Pré-requisitos

- [uv](https://docs.astral.sh/uv/) instalado
- Docker e Docker Compose (para rodar com Airflow)
- Uma chave de API do [OpenWeatherMap](https://openweathermap.org/api)

### Variáveis de ambiente

Crie um arquivo `.env` na pasta `config/` com o seguinte conteúdo:

```env
API_KEY=sua_chave_da_api_openweathermap
```

Para o Docker Compose, crie também um arquivo `.env` na raiz do projeto (usado pelo Airflow), com pelo menos:

```env
AIRFLOW_UID = 501
```

## ▶️ Executando localmente (sem Airflow)

Instale as dependências com `uv`:

```bash
uv sync
```

Execute o pipeline:

```bash
uv run main.py
```

## 🐳 Executando com Airflow (Docker Compose)

Suba os serviços (PostgreSQL, Redis e Airflow):

```bash
docker compose up -d
```

Acesse a interface web do Airflow em [http://localhost:8080](http://localhost:8080) (usuário e senha padrão: `airflow` / `airflow`).

Para encerrar os serviços:

```bash
docker compose down
```

## 📄 Licença

Este projeto utiliza componentes do Apache Airflow, licenciados sob a Apache License 2.0.
