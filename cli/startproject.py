import os

import click
import qprompt

from cli import blocks, utils


@click.command(help="Creates a project directory structure for the given services.")
@click.option("--name", help="Name of the project.", required=True)
@click.option("--directory", help="Destination directory.", required=True)
def startproject(name, directory):
    directory_path = os.path.join(directory, name.lower().replace(" ", "_"))
    utils.create_directory(directory_path)

    # Environment questions
    qprompt.hrule()

    project_environment = {}

    project_environment["django"] = qprompt.ask_yesno(
        msg="Add Django to the environment?"
    )
    project_environment["react"] = qprompt.ask_yesno(
        msg="Add React to the environment?"
    )
    project_environment["geoserver"] = qprompt.ask_yesno(
        msg="Add GeoServer to the environment?"
    )
    project_environment["mapshader"] = qprompt.ask_yesno(
        msg="Add Mapshader to the environment?"
    )
    project_environment["nginx"] = qprompt.ask_yesno(
        msg="Add Nginx to the environment?"
    )

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
        general = blocks.General(
            name="General Files",
            directory_path=directory_path,
            project_name=name,
        )
        general.set_up()

        django = blocks.Django(
            name="Django",
            directory_path=directory_path,
            project_name=name,
        )
        django.set_up()

        if project_environment["redis"]:
            redis = blocks.Redis(
                name="Redis",
                directory_path=directory_path,
                project_name=name,
            )
            redis.set_up()

        if project_environment["celery"]:
            celery = blocks.Celery(
                name="Celery",
                directory_path=directory_path,
                project_name=name,
            )
            celery.set_up()

        if project_environment["react"]:
            react = blocks.React(
                name="React",
                directory_path=directory_path,
                project_name=name,
            )
            react.set_up()

        if project_environment["nginx"]:
            nginx = blocks.Nginx(
                name="Nginx",
                directory_path=directory_path,
                project_name=name,
            )
            nginx.set_up()

    if project_environment["geoserver"]:
        geoserver = blocks.GeoServer(
            name="GeoServer",
            directory_path=directory_path,
            project_name=name,
        )
        geoserver.set_up()

    if project_environment["mapshader"]:
        mapshader = blocks.Mapshader(
            name="Mapshader",
            directory_path=directory_path,
            project_name=name,
        )
        mapshader.set_up()


if __name__ == "__main__":
    startproject()
