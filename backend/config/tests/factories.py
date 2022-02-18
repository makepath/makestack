import factory

from django_celery_results.models import TaskResult


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskResult

    task_id = "123"
    status = "STARTED"
    result = "result"
