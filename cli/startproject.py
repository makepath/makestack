import os

import click
import qprompt

from cli import blocks


@click.command(help="Creates a project directory structure for the given services.")
@click.option("--name", help="Name of the project.", required=True)
@click.option("--directory", help="Destination directory.", required=True)
def startproject(name, directory):
    directory_path = os.path.join(directory, name)
    # utils.create_directory(directory_path)

    # Environment questions
    qprompt.hrule()

    project_environment = {}

    project_environment["django"] = qprompt.ask_yesno(
        msg="Add Django to the environment?"
    )
    # project_environment["react"] = qprompt.ask_yesno(
    #     msg="Add React to the environment?"
    # )
    # project_environment["geoserver"] = qprompt.ask_yesno(
    #     msg="Add GeoServer to the environment?"
    # )
    # project_environment["mapshader"] = qprompt.ask_yesno(
    #     msg="Add Mapshader to the environment?"
    # )
    # project_environment["nginx"] = qprompt.ask_yesno(
    #     msg="Add Nginx to the environment?"
    # )

    if project_environment["django"]:
        project_environment["redis"] = qprompt.ask_yesno(
            msg="Add Redis to the environment?"
        )
        project_environment["celery"] = qprompt.ask_yesno(
            msg="Add Celery to the environment?"
        )

    # Enviroment set up
    qprompt.hrule()
    qprompt.info("Starting to set up the project environment.")

    if project_environment["django"]:
        general = blocks.General(name="General Files", directory_path=directory_path)
        general.set_up()

        django = blocks.Django(name="Django", directory_path=directory_path)
        django.set_up()

        if project_environment["redis"]:
            redis = blocks.Redis(name="Redis", directory_path=directory_path)
            redis.set_up()

        if project_environment["celery"]:
            redis = blocks.Celery(name="Celery", directory_path=directory_path)
            redis.set_up()


if __name__ == "__main__":
    startproject()
