import python_web_io
import argparse


def main(filepath: str, title: str, icon: str, debug: bool):
    """
    Loads the contents of a script and executes it.

    Arguments:
        filepath (str): filepath to script / entrypoint.
    """
    with open(filepath, "r") as file:
        script = file.read()

    # save args to config / Cache
    python_web_io.Cache.set("script", script)
    python_web_io.Cache.set("title", title)
    python_web_io.Cache.set("icon", icon)

    # start the Flask server
    python_web_io.app.run(debug=debug)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a web UI to iteract with a Python script."
    )
    parser.add_argument("filepath", type=str, help="Script filepath (required).")
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
    main(filepath=args.filepath, title=args.title, icon=args.icon, debug=args.debug)
