from src.etl.app.pipeline import run_etl

from unittest.mock import ANY

def test_run_etl_flow(mocker):
    mock_extract = mocker.patch("src.etl.app.pipeline.extract")
    mock_transform = mocker.patch("src.etl.app.pipeline.transform")
    mock_load = mocker.patch("src.etl.app.pipeline.load")

    mock_extract.return_value = [{"a": 1}]
    mock_transform.return_value = "df_fake"

    run_etl("2023-01-01")

    mock_extract.assert_called_once()
    mock_transform.assert_called_once_with([{"a": 1}])
    mock_load.assert_called_once_with("df_fake", ANY)
