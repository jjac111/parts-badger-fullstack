import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.conf.broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "rpc://")
app.conf.accept_content = ["json"]
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"

app.autodiscover_tasks()
