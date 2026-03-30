"""Definição de jobs do Dagster para o orquestrador."""

from dagster import define_asset_job
from dagster._core.definitions.unresolved_asset_job_definition import UnresolvedAssetJobDefinition

etl_job: UnresolvedAssetJobDefinition = define_asset_job(
    name="etl_job"
)
