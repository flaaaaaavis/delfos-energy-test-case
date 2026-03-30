from src.orchestrator.app.jobs import etl_job

def test_job_exists():
    assert etl_job.name == "etl_job"