import argparse

from python_web_io.cache import Cache, load_cache
from python_web_io.server import app


def main(filepath: str, title: str, icon: str, debug: bool):
    """
    Loads the contents of a script and executes it.

    Arguments:
        filepath (str): filepath to script / entrypoint.
    """

    # save args to config / Cache
    Cache.set("source", filepath)
    Cache.set("title", title)
    Cache.set("icon", icon)

    load_cache()

    # start the Flask server
    app.run(debug=debug)


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
    parser.add_argument(
        "--title",
        type=str,
        help="Title for webapp (optional).",
        default="Python Web I/O",
    )
    parser.add_argument(
        "--icon", type=str, help="Emoji webapp icon (optional).", default="🎯"
    )
    args = parser.parse_args()
    main(filepath=args.script, title=args.title, icon=args.icon, debug=args.debug)


if __name__ == "__main__":
    start()
