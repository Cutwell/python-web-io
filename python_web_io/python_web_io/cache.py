import os

class Cache:
    """
    Create a global Cache, to access config variables from multiple Flask sessions.
    """

    __conf = {
        "source": "",      # Python script source
        "script": "",   # Python user script.
        "title": "",    # Title for the tab / form
        "icon": "",     # Emoji icon for the tab / website
        "last_read_time": 0,    # Epoch time of last file access
    }
    __setters = ["source", "script", "title", "icon", "last_read_time"]

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
    filepath = Cache.get('source')

    with open(filepath, "r") as file:
        script = file.read()
    
    Cache.set("last_read_time", os.path.getmtime(filepath))
    Cache.set("script", script)
