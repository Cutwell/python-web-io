from flask import session


def input(prompt: str = "Input"):
    """
    Override default input function.

    Update the site HTML with a new input element.
    If prompt, text input. Else, button.
    Wait for callback from API.

    Arguments:
        prompt (str): If the prompt argument is present, it is written to standard output without a trailing newline.

    Returns:
        output (str): The function reads from input, converts it to a string (stripping a trailing newline if present), and returns that.
    """

    session["counter"] += 1
    index = session["counter"] - 1

    if session["counter"] <= len(
        session["io"]
    ):  # if element has recorded input in session
        output = session["io"][index][1][2]
        return output

    else:  # new element
        session["io"].append(("input", (index, prompt)))
        # exit the script exec() early, to prompt user for input
        raise ExecInterrupt


def print(
    *objects, sep: str = " ", end: str = "\n", file: object = None, flush: bool = False
):
    """
    Override default print function.

    Arguments:
        *objects: print objects to the text stream file, separated by sep and followed by end.
        sep (str): string separator to divide multiple objects in output string.
        end (str): string applied to end of output string.
        file (object): file argument must be an object with a write(string) method; if it is not present or None, sys.stdout will be used.
        flush (bool): output buffering is usually determined by file. However, if flush is true, the stream is forcibly flushed.
    """

    session["counter"] += 1

    if session["counter"] > len(session["io"]):  # if new element
        strings = [str(obj) for obj in objects]
        output = f"{sep.join(strings)}{end}"
        session["io"].append(("print", output))


class ExecInterrupt(Exception):
    pass


def Exec(source, globals=None, locals=None):
    try:
        exec(source, globals, locals)
    except ExecInterrupt:
        pass
