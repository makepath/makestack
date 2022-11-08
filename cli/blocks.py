import shutil

import qprompt

from cli import utils


class BaseBlock:
    def __init__(self, name, directory_path, project_name):
        self.name = name
        self.directory_path = directory_path
        self.project_name = project_name

    def _set_up(self):
        pass

    def set_up(self):
        qprompt.status(f"Setting up {self.name}...", self._set_up)


class Django(BaseBlock):
    def _copy_base_folder(self):
        source = "cli/data/django/base"
        destination = f"{self.directory_path}/backend"
        shutil.copytree(source, destination)

    def _copy_docker_folder(self):
        source = "cli/data/django/docker"
        destination = f"{self.directory_path}/docker"
        shutil.copytree(source, destination)

    def _update_project_name(self):
        utils.replace_text_on_file(
            f"{self.directory_path}/backend/config/settings.py",
            "{project_name}",
            self.project_name,
        )

    def _set_up(self):
        self._copy_base_folder()
        self._copy_docker_folder()
        self._update_project_name()


class General(BaseBlock):
    def _copy_base_folder(self):
        source = "cli/data/general"
        destination = f"{self.directory_path}"
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _update_project_name(self):
        treated_project_name = self.directory_path.split("/")[-1]

        utils.replace_text_on_file(
            f"{self.directory_path}/README.md",
            "{project_name}",
            self.project_name,
        )
        utils.replace_text_on_file(
            f"{self.directory_path}/Makefile",
            "{project_name}",
            treated_project_name,
        )
        utils.replace_text_on_file(
            f"{self.directory_path}/docker-compose.yml",
            "{project_name}",
            treated_project_name,
        )

    def _set_up(self):
        self._copy_base_folder()
        self._update_project_name()


class Celery(BaseBlock):
    def _add_env_variables(self):
        envs = "\n# === Celery ===\nCELERY_BROKER_URL=redis://redis:6379\n"
        utils.append_to_file(f"{self.directory_path}/.env", envs)

    def _add_service(self):
        treated_project_name = self.directory_path.split("/")[-1]
        service = utils.get_file_content("cli/data/celery/docker-compose.txt").replace(
            "{project_name}", treated_project_name
        )
        utils.append_to_file(f"{self.directory_path}/docker-compose.yml", service)

    def _add_requirements(self):
        requirements = "\ncelery==5.2.3\ndjango-celery-results==2.2.0"
        utils.append_to_file(
            f"{self.directory_path}/backend/requirements.txt",
            requirements,
        )

    def _add_settings(self):
        app = '    "django_celery_results",'
        settings = (
            "\n\n# Celery\n"
            'CELERY_RESULT_BACKEND = "django-db"\n'
            'CELERY_CACHE_BACKEND = "django-cache"\n'
            "CELERY_TASK_TRACK_STARTED = True\n"
        )

        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/settings.py",
            "THIRD_PARTY_APPS = \[",  # noqa: W605
            app,
        )
        utils.append_to_file(
            f"{self.directory_path}/backend/config/settings.py",
            settings,
        )

    def _add_pytest_plugin(self):
        pytest_plugin = 'pytest_plugins = ("celery.contrib.pytest",)'
        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/conftest.py",
            "from rest_framework.test import APIClient",
            pytest_plugin,
            break_line_before=2,
        )

    def _add_app(self):
        app = (
            "from config.celery import app as celery_app\n"
            "\n"
            '__all__ = ["celery_app"]\n'
        )
        utils.append_to_file(
            f"{self.directory_path}/backend/config/__init__.py",
            app,
        )

    def _add_urls(self):
        urls = (
            "    path(\n"
            '        "tasks/<str:task_id>",\n'
            "        views.TaskRetrieveView.as_view(),\n"
            '        name="task-retrieve",\n'
            "    ),\n"
            '    path("hello_world/", views.HelloWorldView.as_view()),'
        )

        imports = "from config import views"

        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/urls.py",
            "urlpatterns \= \[",  # noqa: W605
            urls,
        )

        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/urls.py",
            "from environs import Env",
            imports,
            break_line_before=1,
        )

    def _add_example_tasks(self):
        utils.copy_file(
            "cli/data/celery/tasks.py",
            f"{self.directory_path}/backend/config/celery.py",
        )

    def _add_views(self):
        imports = (
            "from django_celery_results.models import TaskResult\n"
            "from config.celery import hello_world\n"
            "from config.serializers import TaskSerializer\n"
        )
        views = (
            "\nclass TaskRetrieveView(generics.RetrieveAPIView):\n"
            "    queryset = TaskResult.objects.all()\n"
            "    serializer_class = TaskSerializer\n"
            "    permission_classes = [permissions.AllowAny]\n"
            '    lookup_field = "task_id"\n'
            "\n"
            "\n"
            "class HelloWorldView(APIView):\n"
            "    def get(self, request):\n"
            "        task_id = hello_world.delay().task_id\n"
            '        content = {"task_id": task_id}\n'
            "        return Response(content)\n"
        )

        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/views.py",
            "from rest_framework.views import APIView  # noqa: F401",
            imports,
            break_line_before=1,
        )
        utils.append_to_file(
            f"{self.directory_path}/backend/config/views.py",
            views,
        )

    def _add_serializers(self):
        imports = "from django_celery_results.models import TaskResult"
        serializers = utils.get_file_content("cli/data/celery/serializers.txt")

        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/serializers.py",
            "from rest_framework import serializers  # noqa: F401",
            imports,
            break_line_before=1,
        )
        utils.append_to_file(
            f"{self.directory_path}/backend/config/serializers.py",
            serializers,
        )

    def _add_tests(self):
        utils.copy_file(
            "cli/data/celery/tests.py",
            f"{self.directory_path}/backend/config/tests/test_celery.py",
        )

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._add_requirements()
        self._add_settings()
        self._add_pytest_plugin()
        self._add_app()
        self._add_urls()
        self._add_example_tasks()
        self._add_views()
        self._add_serializers()
        self._add_tests()


class Redis(BaseBlock):
    def _add_env_variables(self):
        envs = "\n# === Redis ===\nREDIS_SERVER_ADDR=redis:6379\n"
        utils.append_to_file(f"{self.directory_path}/.env", envs)

    def _add_service(self):
        treated_project_name = self.directory_path.split("/")[-1]
        service = utils.get_file_content("cli/data/redis/docker-compose.txt").replace(
            "{project_name}", treated_project_name
        )

        utils.append_to_file(f"{self.directory_path}/docker-compose.yml", service)

    def _add_requirements(self):
        requirements = "\ndjango-redis==5.2.0\nredis==4.1.2"
        utils.append_to_file(
            f"{self.directory_path}/backend/requirements.txt",
            requirements,
        )

    def _add_settings(self):
        settings = (
            "\n\n# Cache\n"
            "CACHES = {\n"
            '    "default": {\n'
            '        "BACKEND": "django_redis.cache.RedisCache",\n'
            '        "LOCATION": "redis://{}".format(env("REDIS_SERVER_ADDR", "localhost:6379")),\n'  # noqa: 501
            '        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},\n'  # noqa: 501
            "    }\n"
            "}\n"
        )
        utils.append_to_file(
            f"{self.directory_path}/backend/config/settings.py",
            settings,
        )

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._add_requirements()
        self._add_settings()
