import os
import builtins

from flask import Flask, session, request, render_template
from python_web_io.override import (
    input,
    print,
    Exec,
)  # input, print are listed as unused, but exist to override builtin calls made from Exec() of the user script
from python_web_io.cache import Cache

app = Flask(__name__)

FLASK_SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
app.secret_key = bytes(FLASK_SECRET_KEY, "utf-8")


@app.errorhandler(500)
def internal_error(error):
    """
    If the user was part-way through submitting a form when the server dies, and does not close the browser tab to clear session cookies, the app may get confused due to a mismatch between server session and user progress.
    A custom 500 error page should inform the user of this issue and direct them to clear cookies / close the tab to fix.
    """

    return render_template("500.html", error=error)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Run a Python script, generating a list of IO to display.
    Stop execution after finding an input without cached response (in session storage).
    Display list of IO to client, prompt for the next input.

    Returns:
        html: Rendered index.html page, displaying the user input as reached so far.
    """

    # POST request indicates user is submitting input
    if request.method == "POST":
        # iterate the form inputs/submission
        # we don't support re-editing previous submissions yet (past inputs are disabled), but this approach could allow this to change in the future
        for key, value in request.form.items():
            index = int(key)

            # assert does not have value assigned (raise error if already assigned, as key error or client enabling disabled inputs)
            assert len(session["io"][index][1]) == 2
            # if passing, reassign io element with a value arg
            session["io"][index] = ("input", (*session["io"][index][1], value))

    # track input/print elements encountered over multiple re-runs of the script
    if "io" not in session:
        session["io"] = []

    # use a counter to track number of elements encountered in this script rerun
    session["counter"] = 0

    # execute the user script to collect IO elements
    # if an unencountered input is found, the script terminates early and the user is prompted to provide input
    Exec(Cache.get("script"))

    # render collected IO into a form - inputs with submitted values are disabled
    return render_template(
        "index.html", title=Cache.get("title"), icon=Cache.get("icon"), io=session["io"]
    )


if __name__ == "__main__":
    app.run(debug=True)
