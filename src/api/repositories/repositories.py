from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.models import Data


async def get_data(
    db: AsyncSession,
    start,
    end,
    variables,
    limit,
    offset
):
    query = (
        select(Data)
        .where(Data.timestamp >= start)
        .where(Data.timestamp <= end)
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(query)
    rows = result.scalars().all()

    output = []

    for row in rows:
        item = {"timestamp": row.timestamp}

        for var in variables:
            item[var] = getattr(row, var)

        output.append(item)

    return output