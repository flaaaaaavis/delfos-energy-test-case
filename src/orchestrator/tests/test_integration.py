from dagster import materialize
from ..app.assets import etl_asset

def test_asset_materialization(mocker):
    mocker.patch("src.etl.app.pipeline.extract", return_value=[])
    mocker.patch("src.etl.app.pipeline.transform", return_value=[])
    mocker.patch("src.etl.app.pipeline.load", return_value=None)

    result = materialize(
        [etl_asset],
        partition_key="2023-01-01",
        resources={
            "api_url": "http://fake-api",
            "target_db": "sqlite:///:memory:"
        }
    )

    assert result.success