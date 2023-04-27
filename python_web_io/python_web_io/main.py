import argparse
import os
import toml
import logging


from python_web_io.cache import Cache, load_cache
from python_web_io.server import app


def main(filepath: str = None, debug: bool = False):
    """
    Loads the contents of a script and executes it.

    Arguments:
        filepath (str): filepath to script / entrypoint.
    """

    # look for a .pythonwebio directory containing a config.toml file.
    if os.path.exists(".pythonwebio/config.toml") and os.path.isfile(
        ".pythonwebio/config.toml"
    ):
        with open(".pythonwebio/config.toml", "r") as file:
            # parse toml into config dict
            config = toml.loads(file.read())

        if config["page"]:
            Cache.set("page", config["page"])
            # if css set and is string, wrap as list
            if config["page"]["css"] and isinstance(config["page"]["css"], str):
                config["page"]["css"] = [
                    config["page"]["css"],
                ]

        if config["about"]:
            Cache.set("about", config["about"])

        if config["project"]:
            Cache.set("project", config["project"])

        if config["script"]:
            Cache.set("script", config["script"])

        debug = (
            (debug or config["flask"]["debug"]) if config["flask"]["debug"] else debug
        )
        host = config["flask"]["host"] if config["flask"]["host"] else "127.0.0.1"
        port = config["flask"]["port"] if config["flask"]["port"] else 5000

    # allow cli override
    if filepath:
        script = Cache.get("script")
        entrypoint = script["entrypoint"] if script["entrypoint"] else None
        Cache.set("script", {"entrypoint": entrypoint, "filepath": filepath})

    load_cache()

    if debug:  # enable debug logging
        logging.basicConfig(level=logging.DEBUG)

    # start the Flask server
    app.run(host=host, port=port, debug=debug)


def start():
    parser = argparse.ArgumentParser(
        description="Generate a web UI to iteract with a Python script."
    )
    parser.add_argument("script", type=str, help="Script filepath (required).")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Boolean switch to debug the Flask server (True if flagged) (optional).",
    )
    args = parser.parse_args()
    main(filepath=args.script, debug=args.debug)


if __name__ == "__main__":
    start()
