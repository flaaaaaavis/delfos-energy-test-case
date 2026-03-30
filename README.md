# 🚀 Delfos Energy – ETL Pipeline

![Docker](https://img.shields.io/badge/docker-ready-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/api-fastapi-009688)
![Dagster](https://img.shields.io/badge/orchestration-dagster-purple)
![PostgreSQL](https://img.shields.io/badge/database-postgresql-336791)
![Status](https://img.shields.io/badge/status-active-green)

---

## 📌 Visão Geral

Delfos Energy é um sistema completo de **ETL (Extract, Transform, Load)** para análise de dados de energia eólica. O projeto implementa uma arquitetura em camadas com:

- 🗄️ **API REST (FastAPI)** — Acesso aos dados brutos da fonte
- 📊 **Pipeline ETL** — Extração, transformação e carga de dados
- 🗂️ **Dois bancos PostgreSQL** — Fonte (dados brutos) e Alvo (dados processados)
- 🎯 **Orquestração Dagster** — Agendamento e execução de tarefas
- ✅ **Testes automatizados** — Cobertura para API, ETL e orquestração

---

## 🧱 Arquitetura

```mermaid
graph TB
    A[(Source DB<br/>PostgreSQL)] --> B["FastAPI<br/>localhost:8000"]
    B --> C["ETL<br/>Pipeline"]
    C --> D[(Target DB<br/>PostgreSQL)]
    E["Dagster<br/>localhost:3000"] -->|Orquestra| C
    style A fill:#336791,color:#fff
    style D fill:#336791,color:#fff
    style B fill:#009688,color:#fff
    style C fill:#4CAF50,color:#fff
    style E fill:#9C27B0,color:#fff
```

---

## 📁 Estrutura do Projeto

```
delfos-energy-test-case/
├── src/
│   ├── api/                    # API REST (FastAPI)
│   │   ├── main.py            # Aplicação FastAPI
│   │   ├── core/              # Configurações
│   │   │   ├── settings.py
│   │   │   ├── database.py
│   │   │   └── logger.py
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── repositories/       # Data Access Layer
│   │   ├── routes/            # Endpoints da API
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── scripts/           # Scripts utilitários (seed.py)
│   │   └── tests/             # Testes unitários da API
│   │
│   ├── etl/                   # Pipeline ETL
│   │   ├── app/
│   │   │   ├── pipeline.py    # Orquestração E → T → L
│   │   │   ├── extract.py     # Extração de dados
│   │   │   ├── transform.py   # Transformação de dados
│   │   │   ├── load.py        # Carregamento de dados
│   │   │   └── config.py      # Configurações
│   │   └── tests/             # Testes unitários do ETL
│   │
│   └── orchestrator/           # Orquestração (Dagster)
│       ├── app/
│       │   ├── definitions.py # Configuração Dagster
│       │   ├── assets.py      # Assets particionados
│       │   ├── jobs.py        # Jobs de execução
│       │   ├── schedules.py   # Agendamentos
│       │   └── resources.py   # Recursos (API, DB)
│       └── tests/             # Testes de orquestração
│
├── docker-compose.yml         # Orquestração de containers
├── requirements.txt           # Dependências Python
├── .env                       # Variáveis de ambiente
└── README.md                  # Este arquivo
```

---

## 🗄️ Bancos de Dados

### 🔹 Banco Fonte (Source DB)

**Banco:** `source_db` (Porta: 5433)

**Tabela:** `data`

| Coluna              | Tipo      | Descrição                          |
| ------------------- | --------- | ---------------------------------- |
| `id`                | INTEGER   | Identificador único (PK)           |
| `timestamp`         | TIMESTAMP | Data/hora do registro              |
| `wind_speed`        | FLOAT     | Velocidade do vento (m/s)          |
| `power`             | FLOAT     | Potência gerada (MW)               |
| `ambient_temperature` | FLOAT   | Temperatura ambiente (°C)          |

**Características:**
- Frequência de coleta: **1 minuto**
- Intervalo de dados: **10 dias**
- Dados gerados via script `seed.py` para testes
- Total aprox.: 14.400 registros

---

### 🔹 Banco Alvo (Target DB)

**Banco:** `target_db` (Porta: 5434)

**Tabela:** `signal`

| Coluna | Tipo    | Descrição              |
| ------ | ------- | ---------------------- |
| `id`   | INTEGER | Identificador único    |
| `name` | TEXT    | Nome do sinal          |

**Tabela:** `data`

| Coluna      | Tipo      | Descrição              |
| ----------- | --------- | ---------------------- |
| `timestamp` | TIMESTAMP | Momento do agregado    |
| `signal_id` | INTEGER   | FK para `signal.id`    |
| `mean`      | FLOAT     | Média do intervalo     |
| `min`       | FLOAT     | Mínimo do intervalo    |
| `max`       | FLOAT     | Máximo do intervalo    |
| `stddev`    | FLOAT     | Desvio padrão          |

**Características:**
- Dados **agregados cada 10 minutos**
- Sinais: `wind_speed`, `power`, `ambient_temperature`
- Métricas calculadas: mean, min, max, stddev

---

## ⚙️ Pipeline ETL

O pipeline implementa o padrão clássico de ETL com separação clara entre as etapas:

### 🔹 Extract (`extract.py`)

Consome dados da API REST:
- **Endpoint:** `GET /data?start=<date>&end=<date>&variables=<vars>`
- **Método:** HTTP
- **Filtros:** Intervalo de datas
- **Variáveis extraídas:**
  - `wind_speed` — Velocidade do vento
  - `power` — Potência
  - `ambient_temperature` — Temperatura

**Output:** DataFrame com registros brutos

---

### 🔹 Transform (`transform.py`)

Processa os dados brutos:
- Agregação em janelas de **10 minutos**
- Cálculo de estatísticas por janela:
  - `mean` — Média
  - `min` — Valor mínimo
  - `max` — Valor máximo
  - `stddev` — Desvio padrão
- Tratamento de valores nulos
- Validação de qualidade

**Output:** DataFrame transformado e validado

---

### 🔹 Load (`load.py`)

Persiste dados no banco alvo:
- **Banco:** PostgreSQL (target_db)
- **Método:** SQLAlchemy ORM
- **Operações:** INSERT batch
- **Transações:** Atômicas com rollback

**Output:** Confirma carga bem-sucedida

---

### 🔹 Pipeline Completo (`pipeline.py`)

Orquestra E → T → L:
```python
def run_etl_pipeline(start_date, end_date):
    raw_data = extract(start_date, end_date)
    transformed = transform(raw_data)
    load(transformed)
```

**Observação:** Pode ser executado manualmente via Python ou via Dagster

---

## 🎯 Orquestração com Dagster

**Localização:** `src/orchestrator/app/`

### Componentes

| Arquivo          | Responsabilidade                           |
| ---------------- | ------------------------------------------ |
| `definitions.py` | Configuração principal da orquestração    |
| `assets.py`      | Assets particionados por dia              |
| `jobs.py`        | Jobs de execução do pipeline              |
| `schedules.py`   | Agendamentos (ex: diariamente às 2 AM)   |
| `resources.py`   | Recursos compartilhados (API + DB)       |

### Assets

- **Tipo:** Particionado por dia
- **Trigger:** Manual ou agendado
- **Output:** Dados no banco alvo

### Jobs

Define a execução do pipeline:
```python
@job
def etl_job():
    etl_asset()  # Executa o asset
```

### Schedules

Agendamento automático:
- **Frequência:** Diariamente
- **Horário:** Configurável
- **Timezone:** UTC

### UI Dagster

- **URL:** `http://localhost:3000`
- **Recursos:** Monitoramento, logs, reruns
- **Execução:** Via botão "Materialize"

---

## 🐳 Execução com Docker

### ✅ Pré-requisitos

- **Docker Desktop** (versão 20.10+) — [Download](https://www.docker.com/products/docker-desktop)
- **Docker Compose** (versão 2.0+)
- **Git** — Para clonar o repositório

### 📋 Passo 1: Clone do Repositório

```bash
git clone https://github.com/flaaaaaavis/delfos-energy-test-case.git
cd delfos-energy-test-case
```

### ⚙️ Passo 2: Variáveis de Ambiente

Crie o arquivo `.env` na raiz do projeto:

```env
# PostgreSQL
POSTGRES_USER=user
POSTGRES_PASSWORD=secure_password_here

# Bancos de Dados
SOURCE_DB=source_db
TARGET_DB=target_db
```

**Segurança:** Não comita senhas reais no `.env` — use em desenvolvimento apenas.

### 🚀 Passo 3: Iniciar os Containers

```bash
# Build e start de todos os serviços
docker-compose up --build

# Ou em background (recomendado)
docker-compose up -d --build
```

**Monitorar logs:**
```bash
docker-compose logs -f

# Específico de um serviço
docker-compose logs -f api
docker-compose logs -f etl
docker-compose logs -f orchestrator
```

### 🛑 Parar os Containers

```bash
# Parar serviços sem remover volumes
docker-compose stop

# Parar e remover containers
docker-compose down

# Remover tudo (incluindo volumes)
docker-compose down -v
```

---

## 🌐 Serviços Disponíveis

Após `docker-compose up --build`, os serviços estarão acessíveis:

| Serviço           | URL                      | Descrição                        |
| --------- | ----------------------- | -------------------------------- |
| **API**           | http://localhost:8000   | Docs: `/docs` (Swagger UI)      |
| **Dagster UI**    | http://localhost:3000   | Orquestração e monitoramento    |
| **Source DB**     | localhost:5433          | PostgreSQL com dados brutos     |
| **Target DB**     | localhost:5434          | PostgreSQL com dados agregados  |

**Credenciais Default:**
- Usuário: `user`
- Senha: Definida em `.env`

---

## � Testando a API

### 🔍 Documentação Interativa

Acesse: **http://localhost:8000/docs** (Swagger UI)

### 🧪 Exemplos de Requisições

**1. Listar dados brutos** (com filtros opcionais)

```bash
curl "http://localhost:8000/data?start=2024-01-01&end=2024-01-05&variables=wind_speed,power"
```

**Parâmetros:**
- `start` (string, ISO 8601) — Data inicial
- `end` (string, ISO 8601) — Data final
- `variables` (string[]) — Variáveis (wind_speed, power, ambient_temperature)

**Response:**
```json
{
  "data": [
    {
      "timestamp": "2024-01-01T00:00:00",
      "wind_speed": 5.2,
      "power": 125.3,
      "ambient_temperature": 15.8
    }
  ]
}
```

**2. Dados agregados** (banco alvo)

```bash
curl "http://localhost:8000/aggregated?signal=wind_speed&start=2024-01-01&end=2024-01-05"
```

**Response:**
```json
{
  "data": [
    {
      "timestamp": "2024-01-01T00:10:00",
      "mean": 5.15,
      "min": 4.8,
      "max": 5.6,
      "stddev": 0.25
    }
  ]
}
```

### 🔄 Executar ETL via API

Alguns endpoints permitem triggar o pipeline manualmente (se implementado).

---

## ✅ Testes Automatizados

### Estrutura de Testes

```
src/
├── api/tests/
│   ├── conftest.py         # Fixtures compartilhadas
│   └── test_routes.py      # Testes de endpoints
├── etl/tests/
│   ├── test_extract.py     # Testes de extração
│   ├── test_transform.py   # Testes de transformação
│   ├── test_load.py        # Testes de carregamento
│   └── test_pipeline.py    # Testes de integração
└── orchestrator/tests/
    ├── test_assets.py      # Testes de assets Dagster
    ├── test_jobs.py        # Testes de jobs
    ├── test_schedules.py   # Testes de agendamentos
    └── test_integration.py # Testes fim-a-fim
```

### Executar Testes

**Todos os testes:**
```bash
pytest
```

**Com verbosidade:**
```bash
pytest -v
```

**Específico de um módulo:**
```bash
pytest src/api/tests/
pytest src/etl/tests/
pytest src/orchestrator/tests/
```

**Com coverage:**
```bash
pytest --cov=src --cov-report=html
```

### Fixtures

O arquivo `conftest.py` fornece:
- Banco de dados de teste
- Cliente HTTP mockado
- Connection factories

---

## 🏃 Desenvolvimento Local (sem Docker)

### 1. Configurar Ambiente Python

```bash
# Criar virtual environment
python -m venv .venv

# Ativar
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados

Instale PostgreSQL localmente e crie os bancos:

```bash
psql -U postgres

CREATE DATABASE source_db;
CREATE DATABASE target_db;
```

### 3. Variáveis de Ambiente

Crie `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/source_db
TARGET_DATABASE_URL=postgresql://user:password@localhost:5432/target_db
```

### 4. Executar Serviços

**API:**
```bash
cd src/api
fastapi dev main.py
# http://localhost:8000
```

**ETL (manual):**
```bash
cd src/etl
python -m app.pipeline
```

**Dagster (dev):**
```bash
cd src/orchestrator
dagster dev
# http://localhost:3000
```

---

## 🔐 Boas Práticas Implementadas

✅ **Arquitetura em Camadas**
- API isolada da lógica ETL
- Pipeline ETL desacoplado
- Orquestração independente

✅ **Segurança**
- Credenciais em `.env` (nunca commitadas)
- Senhas do banco não expostas em logs
- Isolamento de containers

✅ **Qualidade de Código**
- Type hints em Python
- Pydantic para validação
- Testes automatizados em todas as camadas

✅ **Reprodutibilidade**
- Docker Compose para ambiente consistente
- `requirements.txt` com versões fixadas
- Seed scripts para dados de teste

✅ **Observabilidade**
- Logs estruturados
- Dagster UI para monitoramento
- Métricas de pipeline

✅ **Boas Práticas DevOps**
- Health checks em containers
- Volumes persistentes
- Versioning de imagens

---

## ⚠️ Observações Importantes

1. **ETL não executa automaticamente** — Inicia via Dagster UI ou manualmente
2. **Dados persistentes** — Volumes Docker mantêm dados entre restarts
3. **Porta do Dagster** — Se 3000 estiver em uso, edite `docker-compose.yml`
4. **Primeira execução** — Seed script popula source_db automaticamente
5. **Performance** — Com 10 dias de dados, Seed leva ~30 segundos

---

## 🐛 Troubleshooting

### ❌ Erro: "Port 5433 already in use"

```bash
# Liberar porta
# Windows:
netstat -ano | findstr :5433
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5433 | xargs kill -9
```

Ou altere em `docker-compose.yml`:
```yaml
source_db:
  ports:
    - "5435:5432"  # Nova porta
```

### ❌ Erro: "Cannot connect to Docker daemon"

```bash
# Docker Desktop não está rodando
# Windows: Inicie o Docker Desktop
# macOS/Linux: systemctl start docker
```

### ❌ Erro: "Service exited with code 1"

```bash
# Verificar logs
docker-compose logs api
docker-compose logs etl

# Rebuild
docker-compose build --no-cache
```

### ❌ Dagster não carrega assets

```bash
# Reinicie o container
docker-compose restart orchestrator

# Ou rebuild
docker-compose build orchestrator
docker-compose up orchestrator
```

### ❌ Banco de dados não inicia

```bash
# Remover volumes antigos
docker-compose down -v

# Reiniciar
docker-compose up --build
```

---

## 📊 Fluxo de Dados Completo

```
1. SEED (Inicial)
   ├─ source_db: tabela 'data' com 14.4k registros (10 dias, 1min freq)
   └─ Timestamp: últimos 10 dias

2. API (Continuous)
   ├─ GET /data → Retorna dados brutos filtrados
   └─ Armazena em memory (não persiste)

3. ETL PIPELINE (On-demand via Dagster)
   ├─ Extract: Chama API, obtém dados
   ├─ Transform: Agrega 10min, calcula stats
   └─ Load: Insere em target_db (tabelas: signal, data)

4. DAGSTER UI
   ├─ Monitora assets e jobs
   ├─ Permite reruns
   └─ Logs detalhados de execução

5. TARGET_DB
   ├─ Dados agregados
   ├─ Pronto para analytics
   └─ Histórico preservado
```

---

## 📚 Recursos Adicionais

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Dagster Documentation](https://docs.dagster.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

## 🤝 Contribuindo

Se encontrar bugs ou tiver sugestões:

1. Abra uma **Issue** descrevendo o problema
2. Crie um **Pull Request** com a solução
3. Siga as convenções do projeto

---

## 📝 Licença

Este projeto está licensiado sob a licença **MIT**. Vejo [LICENSE](LICENSE) para detalhes.

---

## 📞 Suporte

Para dúvidas ou problemas:

- 📧 Abra uma **GitHub Issue**
- 💬 Consulte a dokumentação inline do código
- 🔍 Verifique os logs: `docker-compose logs <serviço>`

---

**Última atualização:** Março 2026
**Versão Python:** 3.11+
**Status:** ✅ Produção-ready
