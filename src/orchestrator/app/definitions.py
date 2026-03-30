from dagster import Definitions

from .assets import etl_asset
from .jobs import etl_job
from .schedules import etl_schedule
from .resources import api_url, target_db

defs = Definitions(
    assets=[etl_asset],
    jobs=[etl_job],
    schedules=[etl_schedule],
    resources={
        "api_url": api_url,
        "target_db": target_db,
    },
)