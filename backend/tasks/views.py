
from celery.result import AsyncResult
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from tasks import example_tasks


class HelloView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        task_id = example_tasks.hello_world.delay().task_id
        content = {"task_id": task_id}
        return Response(content)


class StatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        task_id = request.query_params.get("task_id", None)

        if not task_id:
            return Response(
                {"detail": "task_id is missing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        task_status = AsyncResult(task_id).status
        content = {"task_id": task_id, "task_status": task_status}

        return Response(content)


class ResultView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        task_id = request.query_params.get("task_id", None)

        if not task_id:
            return Response(
                {"detail": "task_id is missing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        task_result = AsyncResult(task_id).get()
        content = {"task_id": task_id, "task_result": task_result}

        return Response(content)
