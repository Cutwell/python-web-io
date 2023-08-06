import logging
from flask import (
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
    Blueprint,
)
from ..cache import has_cache_expired, load_cache
from ..override import (
    Entry,
    Exec,
    Input,
    Print,
)

from .. import cache_config


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.errorhandler(500)
def internal_error(error):
    """
    If the user was part-way through submitting a form when the server dies, and does not close the browser tab to clear session cookies, the app may get confused due to a mismatch between server session and user progress.
    A custom 500 error page should inform the user of this issue and direct them to clear cookies / close the tab to fix.
    """

    return render_template("500.html", page=cache_config.get("page"), error=error)


@home_bp.route("/", methods=["GET", "POST"])
@home_bp.route("/index", methods=["GET", "POST"])
def index():
    """
    Run a Python script, generating a list of IO to display.
    Stop execution after finding an input without cached response (in session storage).
    Display list of IO to client, prompt for the next input.

    Returns:
        html: Rendered index.html page, displaying the user input as reached so far.
    """

    # check if cached script has expired (has script been modified since we read from it?)
    if has_cache_expired(cache_config):
        logging.info("Refreshing expired cache.")
        # reset session
        session["io"] = []

        # reload script into Cache
        load_cache(cache_config)

    # POST request indicates user is submitting input
    elif request.method == "POST":
        if len(request.form) > 0:
            # consilidate key-value pairs for duplicate keys
            form = request.form.to_dict(flat=False)
            # if form has data
            # iterate the form inputs/submission
            # we don't support re-editing previous submissions yet (past inputs are disabled), but this approach could allow this to change in the future
            for key, value in form.items():
                index = int(key)
                # unwrap list if single item, else keep as list
                value = value[0] if len(value) == 1 else value

                # if most recent input has no output assigned, set, else this is a form resubmission
                if "output" not in session["io"][index]["attributes"]:
                    # if passing, reassign io element with a value arg
                    session["io"][index]["attributes"]["output"] = value
        else:
            # if form is empty, but submission is made, then set last empty input as None value
            # find index of most recent input by iterating backwards through session stack
            for i in range(1, len(session["io"]) + 1):
                # check if input and magic is "button"
                if (
                    session["io"][-i]["type"] == "input"
                    and "output" not in session["io"][-i]["attributes"]
                ):
                    session["io"][-i]["attributes"]["output"] = None

    # track input/print elements encountered over multiple re-runs of the script
    if "io" not in session:
        session["io"] = []

    # use a counter to track number of elements encountered in this script rerun
    session["counter"] = 0

    # execute the user script to collect IO elements
    # if an unencountered input is found, the script terminates early and the user is prompted to provide input
    namespace = {"print": Print, "input": Input}
    error = Exec(cache_config.get("code"), namespace)

    # if an entrypoint is defined, run that function (from the created namespace)
    script = cache_config.get("script")
    if "entrypoint" in script:
        Entry(namespace[script["entrypoint"]])

    # if error raised, then previous input is likely invalid
    # find last input and delete user input (and delete any elements past this point)
    if error:
        logging.error(error)
        logging.debug(f"Session stack log: {session['io']}")
        # find index of most recent input by iterating backwards through session stack
        for i in range(1, len(session["io"]) + 1):
            if session["io"][-i]["type"] == "input":
                del session["io"][-i]["type"]["output"]

                # delete all elements past this point
                session["io"] = session["io"][: len(session["io"]) - i + 1]

                break

    # render collected IO into a form - inputs with submitted values are disabled
    return render_template(
        "index.html",
        page=cache_config.get("page"),
        io=session["io"],
        error=error,
        about=cache_config.get("about"),
        project=cache_config.get("project"),
    )


@home_bp.route("/reset", methods=["GET", "POST"])
def reset():
    """
    Reset the user session.
    """
    # clear the user session
    session["io"] = []

    # render collected IO into a form - inputs with submitted values are disabled
    return redirect(url_for("home_bp.index"))


@home_bp.route("/static/<path:path>")
def send_report(path):
    return send_from_directory("static", path)
