import os
import pickle
import functools


class Cache:
    """
    Create a global Cache, to access config variables from multiple Flask sessions.
    """

    __conf = {
        "source": "",  # Python code source (filepath)
        "code": "",  # Python user code (compiled)
        "last_read_time": 0,  # Epoch time of last file access
        "author": {},  # project author, author github link, project description
        "project": {},  # links for license, homepage, bug reporting
        "page": {
            "name": "Python Web I/O",
            "icon": "🎯",
            "css": "https://cdn.jsdelivr.net/npm/water.css@2/out/water.css",
        },  # customisation for name, icon, css href
    }
    __setters = [
        "source",
        "code",
        "name",
        "icon",
        "last_read_time",
        "about",
        "project",
        "page",
    ]

    @staticmethod
    def get(name):
        return Cache.__conf[name]

    @staticmethod
    def set(name, value):
        if name in Cache.__setters:
            Cache.__conf[name] = value
        else:
            raise NameError(
                f"'{name}' not accepted in set() method (reserved for internal use)."
            )


def has_cache_expired():
    """
    Check if a file has been updated since it was last read.

    Args:
        file_path (str): The path of the file to check.
        last_read_time (float): The last time the file was read, in seconds since the epoch.

    Returns:
        bool: True if the file has been updated since it was last read, False otherwise.
    """
    # Get the last modified time of the file
    modified_time = os.path.getmtime(Cache.get("source"))

    # Compare the last modified time with the last read time
    if modified_time > Cache.get("last_read_time"):
        return True
    else:
        return False


def load_cache():
    filepath = Cache.get("source")

    with open(filepath, mode="r", encoding="utf-8") as file:
        code = file.read()

    # compile the code
    compiled_code = compile(code, filepath, "exec")

    Cache.set("last_read_time", os.path.getmtime(filepath))
    Cache.set("code", compiled_code)


def cache_to_file(file_path: str = "cache.pickle"):
    """
    A decorator that caches the output of a function to a file and returns the cached output if the function is called again
    with the same arguments.

    Parameters:
    file_path (str): The path to the file where the cache is stored.

    Returns:
    A decorated function that wraps the original function with caching functionality.

    Examples:
    >>> @cache_to_file('cache.pickle')
    ... def expensive_function(arg):
    ...     # Calculate the result here
    ...     return result

    Notes:
    This wrapper function uses a decorator function that takes the cache file path as an argument and returns another
    decorator function that takes the function to be cached as an argument. The inner decorator function returns a wrapper
    function that checks the cache file for the result of the function call and returns it if it's already in the cache.
    If the result is not in the cache, the wrapper calls the original function to calculate the result, stores the result
    in the cache file, and returns the result.

    The `key` variable in the wrapper function is a hashable tuple that combines the positional and keyword arguments of the
    function call into a single value that can be used as a key for the cache dictionary. The `try` block in the wrapper
    function attempts to load the cache from the file, but if the file is not found or cannot be parsed, it creates
    an empty cache instead.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique key for the function call based on its arguments
            key = str(hash((args, frozenset(kwargs.items()))))

            # Check if the result is already in the cache file
            try:
                with open(file_path, "rb") as f:
                    cache = pickle.load(f)
            except (FileNotFoundError, pickle.UnpicklingError):
                cache = {}
            if key in cache:
                return cache[key]

            # Calculate the result if it's not in the cache
            result = func(*args, **kwargs)

            # Store the result in the cache file for next time
            cache[key] = result
            with open(file_path, "wb") as f:
                pickle.dump(cache, f)

            return result

        return wrapper

    return decorator
