import os
import time

import celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = celery.Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@celery.shared_task(name="hello_world")
def hello_world():
    time.sleep(10)
    return "Hello world."
