from flask import session


def input(prompt: str = "Input", magic: str = "text", magic_attrs: dict = ()):
    """
    Override default input function.

    Update the site HTML with a new input element.
    If prompt, text input. Else, button.
    Wait for callback from API.

    Arguments:
        prompt (str): If the prompt argument is present, it is written to standard output without a trailing newline.
        magic (str): Magic for defining the input element type.
        magic_attrs (dict): Accompanying kwargs for the magic setting, converted to string and used to set element attributes.

    Returns:
        output (str): The function reads from input, converts it to a string (stripping a trailing newline if present), and returns that.
    """

    session["counter"] += 1
    index = session["counter"] - 1

    if session["counter"] <= len(
        session["io"]
    ):  # if element exists for this index
        if len(session["io"][index][1]) == 3:   # if element has recorded input in session
            output = session["io"][index][1][2]
            return output
        else:   # else still waiting on input
            raise ExecInterrupt

    else:  # new element
        magic_attrs = dict_to_string(magic_attrs) if magic_attrs else None
        session["io"].append(("input", (index, prompt), magic, magic_attrs))
        # exit the script exec() early, to prompt user for input
        raise ExecInterrupt


def print(
    *objects, sep: str = " ", end: str = "\n", file: object = None, flush: bool = False, magic: str = "p", magic_attrs: dict = {}
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
        magic_attrs (dict): Accompanying kwargs for the magic setting, converted to string and used to set element attributes.
    """

    session["counter"] += 1

    if session["counter"] > len(session["io"]):  # if new element
        strings = [str(obj) for obj in objects]
        output = f"{sep.join(strings)}{end}"
        magic_attrs = dict_to_string(magic_attrs) if magic_attrs else None
        session["io"].append(("print", output, magic, magic_attrs))


class ExecInterrupt(Exception):
    pass


def Exec(source, globals=None, locals=None):
    try:
        exec(source, globals, locals)
    except ExecInterrupt:
        pass
    except Exception as e:
        return e


def dict_to_string(d):
    """
    Converts a dictionary of key-value pairs into a string with "key=value" format, separated by " ".
    
    Args:
    - d (dict): A dictionary of key-value pairs.
    
    Returns:
    - str: A string with "key=value" format, separated by " ".
    """
    return " ".join([f"{k}={v}" for k, v in d.items()])