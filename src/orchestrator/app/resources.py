"""Definição de recursos do Dagster para o orquestrador."""

from dagster import resource
from sqlalchemy import create_engine
import os

@resource
def api_url(context):
    """Retorna a URL base da API a partir da variável de ambiente API_URL."""
    return os.getenv("API_URL")

@resource
def target_db(context):
    """Cria e retorna um engine SQLAlchemy baseado na variável de ambiente DB_TARGET."""
    db_url = os.getenv("DB_TARGET")
    if not db_url:
        raise ValueError("Environment variable DB_TARGET is not set")
    return create_engine(db_url)