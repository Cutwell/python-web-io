from flask import session
import logging
import markdown


def Input(
    prompt: str = "Input",
    options: list = None,
    **kwargs
):
    """
    Override default input function.

    Update the site HTML with a new input element.
    If prompt, text input. Else, button.
    Wait for callback from API.

    Arguments:
        prompt (str): If present, used as 'value' attribute for element.
        options (list): If present, "prompt" is used as label, and multiple elements of "type" are created.
        kwargs (dict): Accompanying kwargs, used to set element attributes (if "type" not in kwargs, set as default "text"). kwargs with conflicting names (such as "class" can be written as "_class" and the leading "_" will be auto-stripped)

    Returns:
        output (str): The function reads from input, converts it to a string (stripping a trailing newline if present), and returns that.
    """

    attrs = kwargs if kwargs else {}

    # remove leading _ from kwarg keys
    attrs = {k.replace("_", ""):v for k,v in attrs.items()}

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
        # if input type not defined in kwargs, add default
        if "type" not in attrs:
            attrs["type"] = "text"

        session["io"].append(
            {
                "type": "input",
                "attributes": {"index": index, "prompt": prompt},
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
):
    """
    Override default print function. Joins string inputs and interprets as markdown.

    Arguments:
        *objects: print objects to the text stream file, separated by sep and followed by end.
        sep (str): string separator to divide multiple objects in output string.
        end (str): string applied to end of output string.
        file (object): file argument must be an object with a write(string) method; if it is not present or None, sys.stdout will be used.
        flush (bool): output buffering is usually determined by file. However, if flush is true, the stream is forcibly flushed.
    """

    session["counter"] += 1

    # if new element
    if session["counter"] > len(session["io"]):
        strings = [str(obj) for obj in objects]
        output = markdown.markdown(f"{sep.join(strings)}{end}")
        session["io"].append(
            {
                "type": "print",
                "attributes": {"output": output},
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
