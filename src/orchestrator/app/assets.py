"""Definição de assets do Dagster para o pipeline ETL."""


from dagster import asset, DailyPartitionsDefinition
from src.etl.app.pipeline import run_etl

partitions_def = DailyPartitionsDefinition(start_date="2023-01-01")

@asset(partitions_def=partitions_def)
def etl_asset(context):
    """Asset que executa o processo ETL para uma partição de data específica."""
    date = context.partition_key
    run_etl(date)
