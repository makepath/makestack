import pytest
from rest_framework.test import APIClient


pytest_plugins = ("celery.contrib.pytest",)


@pytest.fixture
def client():
    return APIClient()
