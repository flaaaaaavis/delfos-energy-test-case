import pandas as pd



SIGNAL_MAP = {
    "wind_speed": 1,
    "ambient_temperature": 2,
    "power": 3,
}


def transform(raw_data: list[dict]) -> pd.DataFrame:
    """
    Transforma os dados brutos da API em formato long (tidy),
    com colunas: timestamp, signal_id, value.

    Args:
        raw_data (list[dict]): Lista de registros da API.

    Returns:
        pd.DataFrame: DataFrame transformado.
    """

    if not raw_data:
        return pd.DataFrame(columns=["timestamp", "signal_id", "value"])

    df = pd.DataFrame(raw_data)

    if "timestamp" not in df.columns:
        raise ValueError("Campo 'timestamp' não encontrado nos dados")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    value_columns = [col for col in df.columns if col != "timestamp"]

    df_long = df.melt(
        id_vars=["timestamp"],
        value_vars=value_columns,
        var_name="variable",
        value_name="value",
    )

    df_long["signal_id"] = df_long["variable"].map(SIGNAL_MAP)

    df_long = df_long.drop(columns=["variable"])

    df_long = df_long.sort_values(by=["signal_id", "timestamp"]).reset_index(drop=True)

    return df_long