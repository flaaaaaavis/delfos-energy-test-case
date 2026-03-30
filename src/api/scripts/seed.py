"""Script para popular o banco de dados com dados sintéticos iniciais."""

from datetime import datetime
import pandas as pd
import numpy as np
from sqlalchemy import text

from src.api.core.database import SessionLocal
from src.api.models.models import Data


async def seed_data():
    """
    Gera e insere dados históricos fictícios no banco de dados caso a tabela esteja vazia.
    Cria registros de 10 dias com granularidade de 1 minuto.
    """
    async with SessionLocal() as db:
        result = await db.execute(text("SELECT COUNT(*) FROM data"))
        count = result.scalar()

        if count and count > 0:
            return

        start = datetime(2025, 1, 1)
        periods = 10 * 24 * 60  # 10 dias

        rng = pd.date_range(start=start, periods=periods, freq="1min")

        df = pd.DataFrame({
            "timestamp": rng,
            "wind_speed": np.random.uniform(0, 20, size=periods),
            "power": np.random.uniform(0, 1000, size=periods),
            "ambient_temperature": np.random.uniform(15, 35, size=periods),
        })

        records = df.to_dict(orient="records")

        db.add_all([Data(**{str(k): v for k, v in r.items()}) for r in records])
        await db.commit()
