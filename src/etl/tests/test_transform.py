import pandas as pd
from src.etl.app.transform import transform


def test_transform_success():
    raw_data = [
        {"timestamp": "2023-01-01T00:00:00", "wind_speed": 10, "power": 100},
        {"timestamp": "2023-01-01T01:00:00", "wind_speed": 12, "power": 120},
    ]

    df = transform(raw_data)

    assert "timestamp" in df.columns
    assert "signal_id" in df.columns
    assert "value" in df.columns

    assert not df.empty


def test_transform_empty():
    df = transform([])

    assert df.empty
