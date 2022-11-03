import shutil

import qprompt

from cli import utils


class BaseBlock():
    def __init__(self, name, directory_path):
        self.name = name
        self.directory_path = directory_path

    def _set_up(self):
        pass

    def set_up(self):
        qprompt.status(f"Setting up {self.name}...", self._set_up)


class Django(BaseBlock):
    def _copy_base_folder(self):
        source = "cli/data/django"
        destination = f"{self.directory_path}/backend"
        shutil.copytree(source, destination)

    def _update_project_name(self):
        project_name = self.directory_path.split("/")[-1]
        utils.replace_text_on_file(
            f"{self.directory_path}/backend/config/settings.py",
            "{project_name}", 
            project_name
        )

    def _set_up(self):
        self._copy_base_folder()
        self._update_project_name()


class General(BaseBlock):
    def _copy_base_folder(self):
        source = "cli/data/general"
        destination = f"{self.directory_path}"
        shutil.copytree(source, destination)

    def _update_project_name(self):
        project_name = self.directory_path.split("/")[-1]
        utils.replace_text_on_file(
            f"{self.directory_path}/README.md",
            "{project_name}", 
            project_name
        )

    def _set_up(self):
        self._copy_base_folder()
        self._update_project_name()


class Celery(BaseBlock):
    def _add_env_variables(self):
        envs = """
        # === Celery ===
        CELERY_BROKER_URL=redis://redis:6379
        """
        utils.append_to_file(f"{self.directory_path}/.env", envs)

    def _add_service(self):
        service = utils.get_file_content("cli/data/celery/docker-compose.txt")
        utils.append_to_file(
            f"{self.directory_path}/docker-compose.yml",
            service
        )

    def _add_requirements(self):
        requirements = """
        celery==5.2.3
        django-celery-results==2.2.0
        """
        utils.append_to_file(
            f"{self.directory_path}/backend/requirements.txt",
            requirements
        )

    def _add_pytest_plugin(self):
        pytest_plugin = """
        pytest_plugins = ("celery.contrib.pytest",)
        """
        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/conftest.py",
            "from rest_framework.test import APIClient",
            pytest_plugin,
            break_line_before=2
        )

    def _add_app(self):
        app = """
        from config.celery import app as celery_app

        __all__ = ["celery_app"]
        """
        utils.append_to_file(
            f"{self.directory_path}/backend/config/__init__.py",
            app
        )


    def _create_example_tasks(self):
        content = """
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
        """
        utils.append_to_file(
            f"{self.directory_path}/backend/config/celery.py",
            content
        )

    def _create_tests(self):
        content = """
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
        """
        utils.append_to_file(
            f"{self.directory_path}/backend/config/tests/test_celery.py",
            content
        )

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._add_requirements()
        self._add_pytest_plugin()
        self._add_app()
        self._create_example_tasks()
        self._create_tests()


class Redis(BaseBlock):
    def _add_env_variables(self):
        envs = """
        # === Redis ===
        REDIS_SERVER_ADDR=redis:6379
        """
        utils.append_to_file(f"{self.directory_path}/.env", envs)

    def _add_service(self):
        service = utils.get_file_content("cli/data/redis/docker-compose.txt")

        utils.append_to_file(f"{self.directory_path}/docker-compose.yml", service)

    def _add_requirements(self):
        requirements = """
        django-redis==5.2.0
        redis==4.1.2
        """
        utils.append_to_file(f"{self.directory_path}/backend/requirements.txt", requirements)

    def _add_settings(self):
        settings = """
        # Cache
        CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://{}".format(env("REDIS_SERVER_ADDR", "localhost:6379")),
                "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            }
        }
        """
        utils.append_to_file(f"{self.directory_path}/backend/config/settings.py", settings)

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._add_requirements()
        self._add_settings()