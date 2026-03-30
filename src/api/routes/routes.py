"""Definição das rotas da API para consulta de dados."""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.core import settings

from ..core.database import get_db
from ..core.logger import logger
from ..repositories.repositories import get_data

router = APIRouter()

@router.get("/data")


async def read_data(
    start: datetime,
    end: datetime,
    vars: List[str] = Query(...),
    page: int = 1,
    page_size: int = settings.settings.default_page_size,
    db: AsyncSession = Depends(get_db)
):
    """
    Consulta dados históricos filtrados por período e variáveis específicas.

    Args:
        start (datetime): Data e hora de início.
        end (datetime): Data e hora de fim.
        vars (List[str]): Lista de variáveis a serem retornadas.
        page (int): Número da página para paginação.
        page_size (int): Quantidade de registros por página.
        db (AsyncSession): Sessão do banco de dados.
    """

    # validação de variáveis
    invalid_vars = set(vars) - settings.settings.allowed_variables
    if invalid_vars:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid variables: {invalid_vars}"
        )

    # validação de paginação
    if page_size > settings.settings.max_page_size:
        raise HTTPException(status_code=400, detail="Page size too large")

    offset = (page - 1) * page_size

    logger.info(f"Fetching data | start={start} end={end} vars={vars}")

    data = await get_data(
        db,
        start,
        end,
        vars,
        page_size,
        offset
    )

    return {
        "page": page,
        "page_size": page_size,
        "data": data
    }
