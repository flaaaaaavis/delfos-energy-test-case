"""Configuração de conexão com o banco de dados da aplicação."""


from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base

from .settings import settings


engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Gera uma nova sessão assíncrona do banco de dados para cada requisição.

    Yields:
        AsyncSession: Sessão do SQLAlchemy para operações assíncronas.
    """
    async with SessionLocal() as session:
        yield session
