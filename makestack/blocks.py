import shutil

import qprompt

from makestack import utils


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
        source = "makestack/data/django/base"
        destination = f"{self.directory_path}/backend"
        shutil.copytree(source, destination)

    def _copy_docker_folder(self):
        source = "makestack/data/django/docker"
        destination = f"{self.directory_path}/docker"
        shutil.copytree(source, destination)

    def _copy_deploy_folder(self):
        dev_source = "makestack/data/django/deploy/dev"
        dev_destination = f"{self.directory_path}/deploy/dev"
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = "makestack/data/django/deploy/prod"
        prod_destination = f"{self.directory_path}/deploy/prod"
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _update_project_name(self):
        utils.replace_text_on_file(
            f"{self.directory_path}/backend/config/settings.py",
            "{project_name}",
            self.project_name,
        )

    def _set_up(self):
        self._copy_base_folder()
        self._copy_docker_folder()
        self._copy_deploy_folder()
        self._update_project_name()


class General(BaseBlock):
    def _copy_base_folder(self):
        source = "makestack/data/general"
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
        service = utils.get_file_content(
            "makestack/data/celery/docker-compose.txt"
        ).replace("{project_name}", treated_project_name)
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
            "makestack/data/celery/tasks.py",
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
        serializers = utils.get_file_content("makestack/data/celery/serializers.txt")

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

    def _add_factories(self):
        imports = "from django_celery_results.models import TaskResult"
        factories = utils.get_file_content("makestack/data/celery/factories.txt")

        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/tests/factories.py",
            "import factory  # noqa: F401",
            imports,
            break_line_before=1,
        )
        utils.append_to_file(
            f"{self.directory_path}/backend/config/tests/factories.py",
            factories,
        )

    def _add_tests(self):
        utils.copy_file(
            "makestack/data/celery/tests.py",
            f"{self.directory_path}/backend/config/tests/test_celery.py",
        )

    def _copy_deploy_folder(self):
        dev_source = "makestack/data/celery/deploy/dev"
        dev_destination = f"{self.directory_path}/deploy/dev"
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = "makestack/data/celery/deploy/prod"
        prod_destination = f"{self.directory_path}/deploy/prod"
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

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
        self._add_factories()
        self._add_tests()
        self._copy_deploy_folder()


class Redis(BaseBlock):
    def _add_env_variables(self):
        envs = "\n# === Redis ===\nREDIS_SERVER_ADDR=redis:6379\n"
        utils.append_to_file(f"{self.directory_path}/.env", envs)

    def _add_service(self):
        service = utils.get_file_content("makestack/data/redis/docker-compose.txt")

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

    def _copy_deploy_folder(self):
        dev_source = "makestack/data/redis/deploy/dev"
        dev_destination = f"{self.directory_path}/deploy/dev"
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = "makestack/data/redis/deploy/prod"
        prod_destination = f"{self.directory_path}/deploy/prod"
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._add_requirements()
        self._add_settings()
        self._copy_deploy_folder()


class React(BaseBlock):
    def _copy_base_folder(self):
        source = "makestack/data/react/base"
        destination = f"{self.directory_path}/frontend"
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _add_make_command(self):
        make_command = utils.get_file_content("makestack/data/react/make_command.txt")
        utils.append_to_file_after_matching(
            f"{self.directory_path}/Makefile",
            "\$\(ENTER_BACKEND\) pytest",  # noqa: W605 W291
            make_command,
            break_line_before=1,
        )

        utils.replace_text_on_file(
            f"{self.directory_path}/Makefile",
            "build\:",  # noqa: W605
            "build: build-frontend",
        )

    def _add_settings(self):
        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/settings.py",
            "LOCAL_APPS \= \[",  # noqa: W605
            '    "frontend",',
        )
        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/settings.py",
            '        "DIRS"\: \[',  # noqa: W605
            '            os.path.join(BASE_DIR, "frontend"),',
        )
        utils.append_to_file_after_matching(
            f"{self.directory_path}/backend/config/settings.py",
            "STATICFILES_DIRS \= \[",  # noqa: W605
            '    os.path.join(BASE_DIR, "frontend", "static"),',
        )

    def _add_url(self):
        utils.append_to_file(
            f"{self.directory_path}/backend/config/urls.py",
            '\nurlpatterns += [re_path(r"^", views.ReactAppView.as_view())]\n',
        )

    def _add_view(self):
        view_content = utils.get_file_content("makestack/data/react/view.txt")
        view_imports_content = utils.get_file_content(
            "makestack/data/react/view_imports.txt"
        )

        utils.append_to_file(
            f"{self.directory_path}/backend/config/views.py",
            view_content,
        )
        utils.append_to_file_top(
            f"{self.directory_path}/backend/config/views.py",
            view_imports_content,
        )

    def _copy_docker_folder(self):
        source = "makestack/data/react/docker"
        destination = f"{self.directory_path}/docker"
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _set_up(self):
        self._copy_base_folder()
        self._add_make_command()
        self._add_settings()
        self._add_url()
        self._add_view()
        self._copy_docker_folder()


class GeoServer(BaseBlock):
    def _add_env_variables(self):
        content = utils.get_file_content("makestack/data/geoserver/env_vars.txt")
        utils.append_to_file(f"{self.directory_path}/.env", content)

    def _add_service(self):
        service = utils.get_file_content("makestack/data/geoserver/docker-compose.txt")

        utils.append_to_file(f"{self.directory_path}/docker-compose.yml", service)

    def _copy_docker_folder(self):
        source = "makestack/data/geoserver/docker"
        destination = f"{self.directory_path}/docker"
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _copy_deploy_folder(self):
        dev_source = "makestack/data/geoserver/deploy/dev"
        dev_destination = f"{self.directory_path}/deploy/dev"
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = "makestack/data/geoserver/deploy/prod"
        prod_destination = f"{self.directory_path}/deploy/prod"
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._copy_docker_folder()
        self._copy_deploy_folder()


class Mapshader(BaseBlock):
    def _add_service(self):
        service = utils.get_file_content("makestack/data/mapshader/docker-compose.txt")

        utils.append_to_file(f"{self.directory_path}/docker-compose.yml", service)

    def _copy_docker_folder(self):
        source = "makestack/data/mapshader/docker"
        destination = f"{self.directory_path}/docker"
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _copy_deploy_folder(self):
        dev_source = "makestack/data/mapshader/deploy/dev"
        dev_destination = f"{self.directory_path}/deploy/dev"
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = "makestack/data/mapshader/deploy/prod"
        prod_destination = f"{self.directory_path}/deploy/prod"
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _set_up(self):
        self._add_service()
        self._copy_docker_folder()
        self._copy_deploy_folder()


class Nginx(BaseBlock):
    def _add_env_variables(self):
        content = utils.get_file_content("makestack/data/nginx/env_vars.txt")
        utils.append_to_file(f"{self.directory_path}/.env", content)

    def _add_service(self):
        service = utils.get_file_content("makestack/data/nginx/docker-compose.txt")

        utils.append_to_file(f"{self.directory_path}/docker-compose.yml", service)

    def _copy_docker_folder(self):
        source = "makestack/data/nginx/docker"
        destination = f"{self.directory_path}/docker"
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _copy_deploy_folder(self):
        dev_source = "makestack/data/nginx/deploy/dev"
        dev_destination = f"{self.directory_path}/deploy/dev"
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = "makestack/data/nginx/deploy/prod"
        prod_destination = f"{self.directory_path}/deploy/prod"
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._copy_docker_folder()
        self._copy_deploy_folder()


class Terraform(BaseBlock):
    def _copy_base_folder(self):
        source = "makestack/data/terraform"
        destination = f"{self.directory_path}/terraform"
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _set_up(self):
        self._copy_base_folder()


class Sphinx(BaseBlock):
    def _copy_base_folder(self):
        source = "makestack/data/sphinx"
        destination = f"{self.directory_path}/docs"
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _set_up(self):
        self._copy_base_folder()
