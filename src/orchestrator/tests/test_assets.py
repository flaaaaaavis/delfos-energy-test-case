from dagster import build_op_context
from ..app.assets import etl_asset

def test_etl_asset_runs(mocker):
    mock_extract = mocker.patch("src.etl.app.pipeline.extract")
    mock_transform = mocker.patch("src.etl.app.pipeline.transform")
    mock_load = mocker.patch("src.etl.app.pipeline.load")

    mock_extract.return_value = [{"timestamp": "2023-01-01T00:00:00", "wind_speed": 10, "power": 100}]
    mock_transform.return_value = "df_fake"

    context = build_op_context(
        partition_key="2023-01-01",
        resources={
            "api_url": "http://fake-api",
            "target_db": "fake-db"
        }
    )

    etl_asset(context)

    mock_extract.assert_called_once()
    mock_transform.assert_called_once()
    mock_load.assert_called_once()
