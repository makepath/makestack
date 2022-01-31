from functools import partial

from bokeh.embed import components
from bokeh.resources import INLINE
from flask import Flask
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader
from mapshader import hello
from mapshader.flask_app import (
    build_previewer,
    flask_to_geojson,
    flask_to_image,
    flask_to_legend,
    flask_to_tile,
    flask_to_wms,
)
from mapshader.services import get_services
from mapshader.utils import psutil_fetching


jinja2_env = Environment(loader=FileSystemLoader("templates/"))


def index_page(services):
    template = jinja2_env.get_template("index_page.html")

    return template.render(services=services)


def service_page(service):
    plot = build_previewer(service)
    script, div = components(dict(preview=plot))
    template = jinja2_env.get_template("service_page.html")

    resources = INLINE.render()
    html = template.render(resources=resources,
                           script=script,
                           service=service,
                           len=len,
                           div=div)

    return html


def configure_app(app: Flask, user_source_filepath=None, contains=None):

    CORS(app)

    view_func_creators = {
        "tile": flask_to_tile,
        "image": flask_to_image,
        "wms": flask_to_wms,
        "geojson": flask_to_geojson,
        "legend": flask_to_legend,
    }

    services = []
    for service in get_services(
        config_path=user_source_filepath,
        contains=contains
    ):
        services.append(service)

        view_func = view_func_creators[service.service_type]

        # add operational endpoint
        app.add_url_rule(service.service_url,
                         service.name,
                         partial(view_func, source=service.source))
        # add legend endpoint
        app.add_url_rule(
            service.legend_url,
            service.legend_name,
            partial(
                view_func_creators["legend"],
                source=service.source
            )
        )

        # add service page endpoint
        app.add_url_rule(service.service_page_url,
                         service.service_page_name,
                         partial(service_page, service=service))

    app.add_url_rule("/", "home", partial(index_page, services=services))
    app.add_url_rule("/psutil", "psutil", psutil_fetching)

    hello(services)

    return app


def create_app(user_source_filepath=None, contains=None):
    app = Flask(__name__)
    return configure_app(app, user_source_filepath, contains)


if __name__ == "__main__":
    app = create_app().run(host="0.0.0.0", port=3000)
