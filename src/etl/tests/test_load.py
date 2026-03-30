from src.etl.app.load import load


def test_load_calls_to_sql(mocker):
    mock_df = mocker.Mock()
    mock_engine = mocker.Mock()

    load(mock_df, mock_engine)

    mock_df.to_sql.assert_called_once()
