import os
from celery import Celery

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_url = f"redis://{redis_host}:6379/0"

app = Celery(
    "sales_worker",
    broker=redis_url,
    backend=redis_url
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True
)