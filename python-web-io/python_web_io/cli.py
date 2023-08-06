import argparse
from python_web_io.application import init_app


def main(
    config_filepath: str = ".pythonwebio/config.toml",
    script_filepath: str = None,
    debug: bool = False,
):
    """
    Loads the contents of a script and executes it.

    Arguments:
        script_filepath (str): script_filepath to script / entrypoint.
    """

    app = init_app(config_filepath, script_filepath, debug)

    # start the Flask server
    app.run(debug=debug)


def start(*args):
    parser = argparse.ArgumentParser(
        description="Generate a web UI to iteract with a Python script."
    )
    parser.add_argument("--script", type=str, help="Script script_filepath (optional).")
    parser.add_argument(
        "--config",
        type=str,
        help="Script script_filepath (optional).",
        default=".pythonwebio/config.toml",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Boolean switch to debug the Flask server (True if flagged) (optional).",
    )
    args = parser.parse_args()
    main(config_filepath=args.config, script_filepath=args.script, debug=args.debug)


if __name__ == "__main__":
    main()
