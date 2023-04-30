from flask import session
import logging


def Input(
    prompt: str = "Input",
    magic: str = "text",
    attrs: dict = None,
    options: list = None,
):
    """
    Override default input function.

    Update the site HTML with a new input element.
    If prompt, text input. Else, button.
    Wait for callback from API.

    Arguments:
        prompt (str): If the prompt argument is present, it is written to standard output without a trailing newline.
        magic (str): Magic for defining the input element type.
        attrs (dict): Accompanying kwargs for the magic setting, converted to string and used to set element attributes.

    Returns:
        output (str): The function reads from input, converts it to a string (stripping a trailing newline if present), and returns that.
    """

    session["counter"] += 1
    index = session["counter"] - 1

    # if element exists for this index
    if session["counter"] <= len(session["io"]):
        # if element has recorded input in session
        if "output" in session["io"][index]["attributes"]:
            output = session["io"][index]["attributes"]["output"]
            return output
        # else still waiting on input
        else:
            raise ExecInterrupt

    # new element
    else:
        if attrs:
            attrs = dict_to_string(attrs)
        session["io"].append(
            {
                "type": "input",
                "attributes": {"index": index, "prompt": prompt},
                "magic": magic,
                "attrs": attrs,
                "options": options,
            }
        )
        # exit the script exec() early, to prompt user for input
        raise ExecInterrupt


def Print(
    *objects,
    sep: str = " ",
    end: str = "\n",
    file: object = None,
    flush: bool = False,
    magic: str = "p",
    attrs: dict = {},
):
    """
    Override default print function.

    Arguments:
        *objects: print objects to the text stream file, separated by sep and followed by end.
        sep (str): string separator to divide multiple objects in output string.
        end (str): string applied to end of output string.
        file (object): file argument must be an object with a write(string) method; if it is not present or None, sys.stdout will be used.
        flush (bool): output buffering is usually determined by file. However, if flush is true, the stream is forcibly flushed.
        magic (str): Magic for defining the output element tag.
        attrs (dict): Accompanying kwargs for the magic setting, converted to string and used to set element attributes.
    """

    session["counter"] += 1

    # if new element
    if session["counter"] > len(session["io"]):
        strings = [str(obj) for obj in objects]
        output = f"{sep.join(strings)}{end}"
        attrs = dict_to_string(attrs) if attrs else None
        session["io"].append(
            {
                "type": "print",
                "attributes": {"output": output},
                "magic": magic,
                "attrs": attrs,
            }
        )


class ExecInterrupt(Exception):
    pass


def allow_ExecInterrupt(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ExecInterrupt as e:
            logging.debug(e)
        except Exception as e:
            logging.debug(e)

    return wrapper


@allow_ExecInterrupt
def Exec(source, globals=None, locals=None):
    return exec(source, globals, locals)


@allow_ExecInterrupt
def Entry(entry_point):
    return entry_point()


def dict_to_string(d):
    """
    Converts a dictionary of key-value pairs into a string with "key=value" format, separated by " ".

    Args:
    - d (dict): A dictionary of key-value pairs.

    Returns:
    - str: A string with "key=value" format, separated by " ".
    """
    return " ".join([f"{k}={v}" for k, v in d.items()])
