from src.orchestrator.app.resources import api_url, target_db

def test_api_url_resource(monkeypatch):
    monkeypatch.setenv("API_URL", "http://test")

    assert api_url(None) == "http://test"


def test_target_db_resource(monkeypatch):
    monkeypatch.setenv("DB_TARGET", "sqlite:///:memory:")

    engine = target_db(None)
    assert engine is not None