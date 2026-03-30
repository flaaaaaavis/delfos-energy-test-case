"""Definição de agendamentos (schedules) do Dagster."""

from dagster import ScheduleDefinition
from src.orchestrator.app.jobs import etl_job

etl_schedule = ScheduleDefinition(
    job=etl_job,
    cron_schedule="0 1 * * *",  # todo dia 01:00
)