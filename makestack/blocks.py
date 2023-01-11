import os

import shutil

import qprompt

from makestack import utils


class BaseBlock:
    def __init__(self, name, directory_path, project_name):
        self.name = name
        self.directory_path = directory_path
        self.project_name = project_name
        self.here = os.path.dirname(os.path.abspath(__file__))

    def _set_up(self):
        pass

    def set_up(self):
        qprompt.status(f"Setting up {self.name}...", self._set_up)


class Django(BaseBlock):
    def _copy_base_folder(self):
        source = os.path.join(self.here, 'data', 'django', 'base')
        destination = os.path.join(self.directory_path, 'backend')
        shutil.copytree(source, destination)

    def _copy_docker_folder(self):
        source = os.path.join(self.here, 'data', 'django', 'docker')
        destination = os.path.join(self.directory_path, 'docker')
        shutil.copytree(source, destination)

    def _copy_deploy_folder(self):
        dev_source = os.path.join(self.here, 'data', 'django', 'deploy', 'dev')
        dev_destination = os.path.join(self.directory_path, 'deploy', 'dev')
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = os.path.join(self.here, 'data', 'django', 'deploy', 'prod')
        prod_destination = os.path.join(self.directory_path, 'deploy', 'prod')
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
        source = os.path.join(self.here, 'data', 'general')
        destination = self.directory_path
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _update_project_name(self):
        treated_project_name = self.directory_path.split("/")[-1]

        readme = os.path.join(self.directory_path, "README.md")
        utils.replace_text_on_file(
            readme,
            "{project_name}",
            self.project_name,
        )

        makefile = os.path.join(self.directory_path, "Makefile")
        utils.replace_text_on_file(
            makefile,
            "{project_name}",
            treated_project_name,
        )

        docker_compose_file = os.path.join(self.directory_path, "docker-compose.yml")
        utils.replace_text_on_file(
            docker_compose_file,
            "{project_name}",
            treated_project_name,
        )

    def _set_up(self):
        self._copy_base_folder()
        self._update_project_name()


class Celery(BaseBlock):
    def _add_env_variables(self):
        envs = "\n# === Celery ===\nCELERY_BROKER_URL=redis://redis:6379\n"

        env_file = os.path.join(self.directory_path, ".env")
        utils.append_to_file(env_file, envs)

    def _add_service(self):
        treated_project_name = self.directory_path.split("/")[-1]

        docker_compose_txt = os.path.join(self.here, "data",
                                          "celery", "docker-compose.txt")

        service = (utils.get_file_content(docker_compose_txt)
                        .replace("{project_name}", treated_project_name))
        docker_compose_yml = os.path.join(self.directory_path, "docker-compose.yml")
        utils.append_to_file(docker_compose_yml, service)

    def _add_requirements(self):
        requirements = "\ncelery==5.2.3\ndjango-celery-results==2.2.0"
        requirements_file = os.path.join(self.directory_path,
                                         'backend', 'requirements.txt')
        utils.append_to_file(
            requirements_file,
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

        settings_file = os.path.join(self.directory_path,
                                     'backend', 'config', 'settings.py')
        utils.append_to_file_after_matching(
            settings_file,
            "THIRD_PARTY_APPS = \[",  # noqa: W605
            app,
        )
        utils.append_to_file(
            settings_file,
            settings,
        )

    def _add_pytest_plugin(self):
        pytest_plugin = 'pytest_plugins = ("celery.contrib.pytest",)'

        conftest_file = os.path.join(self.directory_path, 'backend', 'conftest.py')
        utils.append_to_file_after_matching(
            conftest_file,
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
        config_init_file = os.path.join(self.directory_path,
                                        'backend',
                                        'config',
                                        '__init__.py')
        utils.append_to_file(
            config_init_file,
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

        config_urls = os.path.join(self.directory_path, 'backend', 'config', 'urls.py')
        utils.append_to_file_after_matching(
            config_urls,
            "urlpatterns \= \[",  # noqa: W605
            urls,
        )

        utils.append_to_file_after_matching(
            config_urls,
            "from environs import Env",
            imports,
            break_line_before=1,
        )

    def _add_example_tasks(self):
        celery_source = os.path.join(self.here, 'data', 'celery', 'tasks.py')
        celery_destination = os.path.join(self.directory_path,
                                          'backend', 'config', 'celery.py')
        utils.copy_file(
            celery_source,
            celery_destination
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

        config_views_file = os.path.join(self.directory_path,
                                         'backend',
                                         'config',
                                         'views.py')
        utils.append_to_file_after_matching(
            config_views_file,
            "from rest_framework.views import APIView  # noqa: F401",
            imports,
            break_line_before=1,
        )
        utils.append_to_file(
            config_views_file,
            views,
        )

    def _add_serializers(self):
        imports = "from django_celery_results.models import TaskResult"

        serializers_source = os.path.join(self.here,
                                          'data', 'celery', 'serializers.txt')
        destination = os.path.join(self.directory_path,
                                   'backend', 'config', 'serializers.py')

        serializers = utils.get_file_content(serializers_source)
        utils.append_to_file_after_matching(
            destination,
            "from rest_framework import serializers  # noqa: F401",
            imports,
            break_line_before=1,
        )
        utils.append_to_file(
            destination,
            serializers,
        )

    def _add_factories(self):
        imports = "from django_celery_results.models import TaskResult"
        factories = os.path.join(self.here, 'data', 'celery', 'factories.txt')
        destination = os.path.join(self.directory_path, 'backend',
                                   'config', 'tests', 'factories.py')

        utils.append_to_file_after_matching(
            destination,
            "import factory  # noqa: F401",
            imports,
            break_line_before=1,
        )
        utils.append_to_file(
            destination,
            factories,
        )

    def _add_tests(self):
        celery_tests = os.path.join(self.here, 'data', 'celery', 'tests.py')
        celery_tests_destination = os.path.join(self.directory_path,
                                                'backend',
                                                'config',
                                                'tests',
                                                'test_celery.py')
        utils.copy_file(
            celery_tests,
            celery_tests_destination
        )

    def _copy_deploy_folder(self):
        dev_source = os.path.join(self.here, 'data', 'celery', 'deploy', 'dev')
        dev_destination = os.path.join(self.directory_path, 'deploy', 'dev')
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = os.path.join(self.here, 'data', 'celery', 'deploy', 'prod')
        prod_destination = os.path.join(self.directory_path, 'deploy', 'prod')
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
        docker_compose_txt = os.path.join(self.here, 'data',
                                          'redis', 'docker-compose.txt')
        service = utils.get_file_content(docker_compose_txt)

        destination = os.path.join(self.directory_path, 'docker-compose.yml')
        utils.append_to_file(destination, service)

    def _add_requirements(self):
        requirements = "\ndjango-redis==5.2.0\nredis==4.1.2"

        requirements_file = os.path.join(self.directory_path,
                                         'backend',
                                         'requirements.txt')
        utils.append_to_file(requirements_file, requirements)

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

        settings_file = os.path.join(self.directory_path,
                                     'backend',
                                     'config',
                                     'settings.py')
        utils.append_to_file(settings_file, settings)

    def _copy_deploy_folder(self):
        dev_source = os.path.join(self.here, 'data', 'redis', 'deploy', 'dev')
        dev_destination = os.path.join(self.directory_path, 'deploy', 'dev')
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = os.path.join(self.here, 'data', 'redis', 'deploy', 'prod')
        prod_destination = os.path.join(self.directory_path, 'deploy', 'prod')
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._add_requirements()
        self._add_settings()
        self._copy_deploy_folder()


class React(BaseBlock):
    def _copy_base_folder(self):
        source = os.path.join(self.here, 'data', 'react', 'base')
        destination = os.path.join(self.directory_path, 'frontend')
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _add_make_command(self):
        make_command_txt = os.path.join(self.here, 'data',
                                        'react', 'make_command.txt')
        make_command = utils.get_file_content(make_command_txt)

        destination = os.path.join(self.directory_path, 'Makefile')
        utils.append_to_file_after_matching(
            destination,
            "\$\(ENTER_BACKEND\) pytest",  # noqa: W605 W291
            make_command,
            break_line_before=1,
        )

        utils.replace_text_on_file(
            destination,
            "build\:",  # noqa: W605
            "build: build-frontend",
        )

    def _add_settings(self):
        settings_file = os.path.join(self.directory_path,
                                     'backend',
                                     'config',
                                     'settings.py')
        utils.append_to_file_after_matching(
            settings_file,
            "LOCAL_APPS \= \[",  # noqa: W605
            '    "frontend",',
        )
        utils.append_to_file_after_matching(
            settings_file,
            '        "DIRS"\: \[',  # noqa: W605
            '            os.path.join(BASE_DIR, "frontend"),',
        )
        utils.append_to_file_after_matching(
            settings_file,
            "STATICFILES_DIRS \= \[",  # noqa: W605
            '    os.path.join(BASE_DIR, "frontend", "static"),',
        )

    def _add_url(self):
        urls_file = os.path.join(self.directory_path,
                                 'backend',
                                 'config',
                                 'urls.py')
        utils.append_to_file(
            urls_file,
            '\nurlpatterns += [re_path(r"^", views.ReactAppView.as_view())]\n',
        )

    def _add_view(self):
        view_txt = os.path.join(self.here, 'data', 'react', 'view.txt')
        view_content = utils.get_file_content(view_txt)

        view_imports = os.path.join(self.here, 'data', 'react', 'view_imports.txt')
        view_imports_content = utils.get_file_content(
            view_imports
        )

        destination = os.path.join(self.directory_path,
                                   'backend',
                                   'config',
                                   'views.py')
        utils.append_to_file(
            destination,
            view_content,
        )
        utils.append_to_file_top(
            destination,
            view_imports_content,
        )

    def _copy_docker_folder(self):
        source = os.path.join(self.here, 'data', 'react', 'docker')
        destination = os.path.join(self.directory_path, 'docker')
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
        source_content = os.path.join(self.here, 'data', 'geoserver', 'env_vars.txt')
        content = utils.get_file_content(source_content)

        destination = os.path.join(self.directory_path, '.env')
        utils.append_to_file(destination, content)

    def _add_service(self):
        docker_compose = os.path.join(self.here,
                                      'data', 'geoserver', 'docker-compose.txt')
        service = utils.get_file_content(docker_compose)

        destination = os.path.join(self.directory_path, 'docker-compose.yml')
        utils.append_to_file(destination, service)

    def _copy_docker_folder(self):
        source = os.path.join(self.here, 'data', 'geoserver', 'docker')
        destination = os.path.join(self.directory_path, 'docker')
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _copy_deploy_folder(self):
        dev_source = os.path.join(self.here, 'data', 'geoserver', 'deploy', 'dev')
        dev_destination = os.path.join(self.directory_path, 'deploy', 'dev')
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = os.path.join(self.here, 'data', 'geoserver', 'deploy', 'prod')
        prod_destination = os.path.join(self.directory_path, 'deploy', 'prod')
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._copy_docker_folder()
        self._copy_deploy_folder()


class Mapshader(BaseBlock):
    def _add_service(self):
        service_file = os.path.join(self.here,
                                    'data', 'mapshader', 'docker-compose.txt')
        service = utils.get_file_content(service_file)

        destination = os.path.join(self.directory_path, 'docker-compose.yml')
        utils.append_to_file(destination, service)

    def _copy_docker_folder(self):
        source = os.path.join(self.here, 'data', 'mapshader', 'docker')
        destination = os.path.join(self.directory_path, 'docker')
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _copy_deploy_folder(self):
        dev_source = os.path.join(self.here, 'data', 'mapshader', 'deploy', 'dev')
        dev_destination = os.path.join(self.directory_path, 'deploy', 'dev')
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = os.path.join(self.here, 'data', 'mapshader', 'deploy', 'prod')
        prod_destination = os.path.join(self.directory_path, 'deploy', 'prod')
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _set_up(self):
        self._add_service()
        self._copy_docker_folder()
        self._copy_deploy_folder()


class Nginx(BaseBlock):
    def _add_env_variables(self):
        source_content = os.path.join(self.here, 'data', 'nginx', 'env_vars.txt')
        content = utils.get_file_content(source_content)

        destination = os.path.join(self.directory_path, '.env')
        utils.append_to_file(destination, content)

    def _add_service(self):
        docker_compose = os.path.join(self.here, 'data', 'nginx', 'docker-compose.txt')
        service = utils.get_file_content(docker_compose)

        destination = os.path.join(self.directory_path, 'docker-compose.yml')
        utils.append_to_file(destination, service)

    def _copy_docker_folder(self):
        source = os.path.join(self.here, 'data', 'nginx', 'docker')
        destination = os.path.join(self.directory_path, 'docker')
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _copy_deploy_folder(self):
        dev_source = os.path.join(self.here, 'data', 'nginx', 'deploy', 'dev')
        dev_destination = os.path.join(self.directory_path, 'deploy', 'dev')
        shutil.copytree(dev_source, dev_destination, dirs_exist_ok=True)

        prod_source = os.path.join(self.here, 'data', 'nginx', 'deploy', 'prod')
        prod_destination = os.path.join(self.directory_path, 'deploy', 'prod')
        shutil.copytree(prod_source, prod_destination, dirs_exist_ok=True)

    def _set_up(self):
        self._add_env_variables()
        self._add_service()
        self._copy_docker_folder()
        self._copy_deploy_folder()


class Terraform(BaseBlock):
    def _copy_base_folder(self):
        source = os.path.join(self.here, 'data', 'terraform')
        destination = os.path.join(self.directory_path, 'terraform')
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _set_up(self):
        self._copy_base_folder()


class Sphinx(BaseBlock):
    def _copy_base_folder(self):
        source = os.path.join(self.here, 'data', 'sphinx')
        destination = os.path.join(self.directory_path, 'docs')
        shutil.copytree(source, destination, dirs_exist_ok=True)

    def _set_up(self):
        self._copy_base_folder()
