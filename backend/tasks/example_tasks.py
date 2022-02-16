import time

from celery import shared_task


@shared_task(name="hello_world")
def hello_world(num=5):
    time.sleep(num)
    return f"Hello world {num}"
