import os

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from django_celery_results.models import TaskResult
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from config.celery import hello_world
from config.serializers import TaskSerializer


class ReactAppView(View):
    def get(self, request):
        with open(
            os.path.join(settings.BASE_DIR, "frontend", "index.html")
        ) as file:
            return HttpResponse(file.read())


class TaskRetrieveView(generics.RetrieveAPIView):
    queryset = TaskResult.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "task_id"


class HelloWorldView(APIView):
    def get(self, request):
        task_id = hello_world.delay().task_id
        content = {"task_id": task_id}
        return Response(content)
