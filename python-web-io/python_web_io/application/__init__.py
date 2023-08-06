from .cache import Cache, load_cache
from .override import Print, Input, ExecInterrupt

from flask import Flask
from flask_session import Session
import os
import toml
import logging


cache_config = Cache()


def init_app(
    config_filepath: str = ".pythonwebio/config.toml",
    script_filepath: str = None,
    debug: bool = False,
):
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_prefixed_env()

    Session(app)

    with app.app_context():
        # Include our Routes
        from .home import routes

        # Register Blueprints
        app.register_blueprint(routes.home_bp)

        # look for a .pythonwebio directory containing a config.toml file.
        if os.path.exists(config_filepath) and os.path.isfile(config_filepath):
            with open(config_filepath, "r") as file:
                # parse toml into config dict
                config = toml.loads(file.read())

            if config["page"]:
                cache_config.set("page", config["page"])
                # if css set and is string, wrap as list
                if config["page"]["css"] and isinstance(config["page"]["css"], str):
                    config["page"]["css"] = [
                        config["page"]["css"],
                    ]

            if config["about"]:
                cache_config.set("about", config["about"])

            if config["project"]:
                cache_config.set("project", config["project"])

            if config["script"]:
                cache_config.set("script", config["script"])

            debug = (
                (debug or config["flask"]["debug"])
                if config["flask"]["debug"]
                else debug
            )
            host = config["flask"]["host"] if config["flask"]["host"] else "127.0.0.1"
            port = config["flask"]["port"] if config["flask"]["port"] else 5000

        # allow cli override
        if script_filepath:
            script = cache_config.get("script")
            entrypoint = script["entrypoint"] if script["entrypoint"] else None
            cache_config.set("script", {"entrypoint": entrypoint, "filepath": script_filepath})

        load_cache(cache_config)

        if debug:
            # enable debug logging
            logging.basicConfig(level=logging.DEBUG)

        return app
