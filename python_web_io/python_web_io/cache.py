class Cache:
    """
    Create a global Cache, to access config variables from multiple Flask sessions.
    """

    __conf = {
        "script": "",   # Python user script.
        "title": "",    # Title for the tab / form
        "icon": "",     # Emoji icon for the tab / website
    }
    __setters = ["script", "title", "icon"]

    @staticmethod
    def get(name):
        return Cache.__conf[name]

    @staticmethod
    def set(name, value):
        if name in Cache.__setters:
            Cache.__conf[name] = value
        else:
            raise NameError(
                "Name not accepted in set() method (reserved for internal use)."
            )
