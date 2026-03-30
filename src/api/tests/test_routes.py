from datetime import datetime, timedelta

from src.api.models.models import Data

import pytest


@pytest.mark.asyncio
async def test_get_data_success(client, db):
    # inserir dados fake
    now = datetime(2025, 1, 1)

    db.add_all([
        Data(
            timestamp=now,
            wind_speed=10,
            power=100,
            ambient_temperature=25
        ),
        Data(
            timestamp=now + timedelta(minutes=1),
            wind_speed=12,
            power=110,
            ambient_temperature=26
        )
    ])
    await db.commit()

    response = await client.get(
        "/data",
        params={
            "start": now.isoformat(),
            "end": (now + timedelta(minutes=5)).isoformat(),
            "vars": ["wind_speed", "power"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert len(data["data"]) == 2
    assert "wind_speed" in data["data"][0]
    assert "power" in data["data"][0]


@pytest.mark.asyncio
async def test_invalid_variable(client):
    response = await client.get(
        "/data",
        params={
            "start": "2025-01-01T00:00:00",
            "end": "2025-01-01T01:00:00",
            "vars": ["invalid_var"]
        }
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_pagination(client, clean_db):
    base = datetime(2025, 1, 1)

    db = clean_db

    # inserir vários registros
    for i in range(20):
        db.add(Data(
            timestamp=base + timedelta(minutes=i),
            wind_speed=i,
            power=i * 10,
            ambient_temperature=20
        ))

    await db.commit()
    
    end_time = base + timedelta(minutes=20)
    response = await client.get(
        "/data",
        params={
            "start": base.isoformat(),
            "end": end_time.isoformat(),
            "vars": ["wind_speed"],
            "page": 1,
            "page_size": 5
        }
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 5