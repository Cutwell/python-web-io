import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

import toml
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starsessions import InMemoryStore, SessionAutoloadMiddleware, SessionMiddleware
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from python_web_io.override import (
    Entry,
    Input,
    Print,
    Run_Path,
)


def update_cached_file_data():
    logging.info("Refreshing expired cache.")
    app.state.script_modified_timestamp = time.time()


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if (
            not event.is_directory and event.src_path == app.state.script["filepath"]
        ):  # Replace with the full path to the Python file
            update_cached_file_data()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ############
    # Startup
    ############

    # define defaults
    app.state.script = {}
    app.state.about = {}
    app.state.project = {}
    app.state.page = {
        "name": "Python Web I/O",
        "icon": "🎯",
        "css": "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css",
    }

    # look for a .pythonwebio directory containing a config.toml file.
    if os.path.exists(app.state.config_path) and os.path.isfile(app.state.config_path):
        with open(app.state.config_path, "r") as file:
            # parse toml into config dict
            config = toml.loads(file.read())

        if config["page"]:
            # if css set and is string, wrap as list
            if config["page"]["css"] and isinstance(config["page"]["css"], str):
                config["page"]["css"] = [
                    config["page"]["css"],
                ]
            app.state.page = config["page"]

        if config["about"]:
            app.state.about = config["about"]

        if config["project"]:
            app.state.project = config["project"]

        if config["script"]:
            app.state.script = config["script"]

        if config["server"] and config["server"]["debug"] is True:
            # enable debug logging
            logging.basicConfig(level=logging.DEBUG)

    # if set, then running in test mode
    if app.state.cli_script_config:
        filepath, entrypoint = app.state.cli_script_config.split(":")
        app.state.script["filepath"] = filepath
        app.state.script["entrypoint"] = entrypoint

    app.state.script_modified_timestamp = time.time()
    update_cached_file_data()

    # Initialize the watchdog observer
    observer = Observer()
    file_change_handler = FileChangeHandler()

    # Start the watchdog observer on app startup
    path = Path(app.state.script["filepath"])
    observer.schedule(file_change_handler, path=path.parent.absolute(), recursive=False)
    observer.start()

    yield  # wait for shutdown

    ############
    # Shutdown
    ############

    # Stop the watchdog observer on app shutdown
    observer.stop()
    observer.join()


app = FastAPI(lifespan=lifespan)
app.secret_key = os.getenv("PYTHON_WEB_IO_SECRET", "")
app.state.cli_script_config = None
app.state.config_path = os.getenv(
    "PYTHON_WEB_IO_CONFIG", ".pythonwebio/config.toml"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionAutoloadMiddleware)
app.add_middleware(SessionMiddleware, store=InMemoryStore())

templates = Jinja2Templates(directory="python_web_io/templates")


def handle_session(session):
    if not session:
        session["counter"] = 0
        session["io"] = []
        session["cached_timestamp"] = time.time()

    if app.state.script_modified_timestamp > session["cached_timestamp"]:
        session["io"] = []
        session["cached_timestamp"] = app.state.script_modified_timestamp


def handle_script(session):
    # use a counter to track number of elements encountered in this script rerun
    session["counter"] = 0

    # execute the user script to collect IO elements
    # if an unencountered input is found, the script terminates early and the user is prompted to provide input
    outputs = Print(session=session)
    inputs = Input(session=session)
    namespace = {"print": outputs.print, "input": inputs.input}
    error = None

    try:
        namespace = Run_Path(
            path_name=app.state.script["filepath"], init_globals=namespace
        )

        # if an entrypoint is defined, run that function (from the created namespace)
        if "entrypoint" in app.state.script:
            Entry(namespace[app.state.script["entrypoint"]])

    # we catch RunPyInterrupt internally within Run_Path() (as this is an allowed error)
    # however all other errors are escalated to this scope
    except Exception as e:
        error = e
        # if error raised, then previous input is likely invalid
        # find last input and delete user input (and delete any elements past this point)
        logging.error(error)
        logging.debug(f"Session stack log: {session['io']}")
        # find index of most recent input by iterating backwards through session stack
        for i in range(1, len(session["io"]) + 1):
            if session["io"][-i]["type"] == "input":
                del session["io"][-i]["type"]["output"]

                # delete all elements past this point
                session["io"] = session["io"][: len(session["io"]) - i + 1]

                break

    return error


@app.get("/index", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
async def get_html_page(request: Request):
    """
    Run a Python script, generating a list of IO to display.
    Stop execution after finding an input without cached response (in session storage).
    Display list of IO to client, prompt for the next input.

    Returns:
            html: Rendered index.html page, displaying the user input as reached so far.
    """

    handle_session(request.session)

    error = handle_script(request.session)

    # render collected IO into a form - inputs with submitted values are disabled
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page": app.state.page,
            "io": request.session["io"],
            "error": error,
            "about": app.state.about,
            "project": app.state.project,
        },
    )


@app.post("/", response_class=HTMLResponse)
@app.post("/index", response_class=HTMLResponse)
async def post_html_page(
    request: Request,
):
    """
    Run a Python script, generating a list of IO to display.
    Stop execution after finding an input without cached response (in session storage).
    Display list of IO to client, prompt for the next input.

    Returns:
            html: Rendered index.html page, displaying the user input as reached so far.
    """

    handle_session(request.session)

    data = await request.form()
    form = jsonable_encoder(data)

    if len(form) > 0:
        # if form has data
        # iterate the form inputs/submission
        # we don't support re-editing previous submissions yet (past inputs are disabled), but this approach could allow this to change in the future
        for key, value in form.items():
            index = int(key)
            # unwrap list if single item, else keep as list
            value = value[0] if len(value) == 1 else value

            # if most recent input has no output assigned, set, else this is a form resubmission
            if "output" not in request.session["io"][index]["attributes"]:
                # if passing, reassign io element with a value arg
                request.session["io"][index]["attributes"]["output"] = value
    else:
        # if form is empty, but submission is made, then set last empty input as None value
        # find index of most recent input by iterating backwards through session stack
        for i in range(1, len(request.session["io"]) + 1):
            # check if input and magic is "button"
            if (
                request.session["io"][-i]["type"] == "input"
                and "output" not in request.session["io"][-i]["attributes"]
            ):
                request.session["io"][-i]["attributes"]["output"] = None

    error = handle_script(request.session)

    # render collected IO into a form - inputs with submitted values are disabled
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page": app.state.page,
            "io": request.session["io"],
            "error": error,
            "about": app.state.about,
            "project": app.state.project,
        },
    )


@app.get("/reset", response_class=RedirectResponse)
@app.post("/reset", response_class=RedirectResponse)
async def reset(request: Request):
    """
    Run a Python script, generating a list of IO to display.
    Stop execution after finding an input without cached response (in session storage).
    Display list of IO to client, prompt for the next input.

    Returns:
            html: Rendered index.html page, displaying the user input as reached so far.
    """

    request.session.clear()

    return "/"


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    If the user was part-way through submitting a form when the server dies, and does not close the browser tab to clear session cookies, the app may get confused due to a mismatch between server session and user progress.
    A custom 500 error page should inform the user of this issue and direct them to clear cookies / close the tab to fix.
    """
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": exc.status_code,
            "detail": exc.detail,
            "page": app.state.page,
        },
        status_code=exc.status_code,
    )


if __name__ == "__main__":
    """
    If running python_web_io/main.py directly (instead of via uvicorn with an entrypoint), accept CLI arguments.
    Ideal for quickly testing capabilities without creating `.envrc` or `.pythonwebio/config.toml` files.
    """

    import argparse
    import uvicorn

    def parse_command_line_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--script",
            type=str,
            default="default_value1",
            help="Set the python script (override `config.toml` settings) (format: e.g.:`path/to/file.py:main`).",
        )
        parser.add_argument(
            "--config",
            type=str,
            default=".pythonwebio/config.toml",
            help="Set the `config.toml` filepath directly (default: `.pythonwebio/config.toml`).",
        )
        parser.add_argument(
            "--host", type=str, default="localhost", help="Host for uvicorn server."
        )
        parser.add_argument(
            "--port", type=int, default=8000, help="Port for uvicorn server."
        )
        return parser.parse_args()

    # Read command-line arguments and set app.state values
    args = parse_command_line_arguments()
    app.state.cli_script_config = args.script
    app.state.config_path = args.config

    uvicorn.run(app, host=args.host, port=args.port)
