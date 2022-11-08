import pytest

from config.tests import factories
from config.celery import hello_world


def test_hello_world():
    result = hello_world()
    expected = "Hello world."

    assert result == expected

@pytest.mark.django_db
def test_hello_world_url(client):
    response = client.get("/hello_world/")
    assert "task_id" in response.json()


@pytest.mark.django_db
def test_tasks_url(client):
    task = factories.TaskFactory()
    task_id = task.task_id

    started_response = client.get(f"/tasks/{task_id}").json()

    task.status = "SUCCESS"
    task.save()

    success_response = client.get(f"/tasks/{task_id}").json()

    assert started_response.get("result") is None
    assert success_response.get("result") == "result"
