from src.orchestrator.app.schedules import etl_schedule

def test_schedule_cron():
    assert etl_schedule.cron_schedule == "0 1 * * *"