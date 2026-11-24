from celery import Celery
from celery.schedules import crontab
from .config import settings
from .pipeline import run_ingestion
celery_app=Celery("jobsense",broker=settings.redis_url,backend=settings.redis_url)
celery_app.conf.timezone="UTC"
celery_app.conf.beat_schedule={"daily-job-refresh":{"task":"app.worker.ingest","schedule":crontab(hour=5,minute=0)}}
@celery_app.task(name="app.worker.ingest",autoretry_for=(Exception,),retry_backoff=True,retry_kwargs={"max_retries":3})
def ingest():return run_ingestion()
@celery_app.task(name="app.worker.manual")
def manual():return run_ingestion()
