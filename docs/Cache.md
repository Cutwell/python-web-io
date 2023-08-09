`python-web-io` works by re-evaluating the target script after each user interaction, to progress the script to the next `input()`, etc.
This means expensive functions may be called more than once per session.
To reduce latency, a cache decorator is made available through the `python_web_io` module.
The `@cache_to_file()` decorator accepts a string argument: `file_path`, which indicates where the cache (a `.pkl` file) should be stored.

```python
import python_web_io as io

@io.cache_to_file('cache.pickle')
def expensive_function(arg):
    # Calculate the result here
    return result
```
