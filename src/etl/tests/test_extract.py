import pytest
import httpx
from src.etl.app.extract import extract


def test_extract_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "data": [
            {"timestamp": "2023-01-01T00:00:00", "wind_speed": 10, "power": 100}
        ]
    }
    mock_response.raise_for_status.return_value = None

    mocker.patch("httpx.get", return_value=mock_response)

    result = extract("2023-01-01", "http://fake-api")

    assert "data" in result
    assert isinstance(result["data"], list)
    assert result["data"][0]["wind_speed"] == 10


def test_extract_http_error(mocker):
    mock_get = mocker.patch("httpx.get")
    mock_get.side_effect = httpx.HTTPError("Erro na API")

    with pytest.raises(httpx.HTTPError):
        extract("2023-01-01", "http://fake-api")
