# Python Web I/O
 Generate a webpage as a GUI for a Python script, and serve from anywhere.

## Usage
```
$ export SECRET_KEY="someSecureSecretKey"
$ python_web_io .\example.py
```
* Create a `.envrc` file, setting `SECRET_KEY` as per [`python_web_io/.envrc.example`](https://github.com/Cutwell/python-web-io/blob/main/python_web_io/.envrc.example).
* Try running the [`example.py`](https://github.com/Cutwell/python-web-io/blob/main/python_web_io/example.py) script using `python_web_io example.py`.

|Argument|||
|:---:|:---:|:---:|
|`"example.py"`|Required|Specify the file path for the app Python script / entrypoint.|
|`--debug`|Optional|Run the Flask server with debug output enabled.|

## Config
### Magic
`input()` and `print()` both support the `magic` keyword argument. For `input()`, `magic` sets the `type` of the input html element. For `print()`, `magic` sets the element type.

||Magic|Default|
|:---:|:---:|:---:|
|`input()`|`button`, `checkbox`, `color`, `date`, `datetime-local`, `email`, `file`, `image`, `month`, `number`, `password`, `radio`, `range`, `search`, `tel`, `text`, `time`, `url`, `week`|`text`|
|`print()`|`style`, `img`, `address`, `footer`, `aside`, `header`, `h1..6`, `blockquote`, `p`, `b`, `abbr`, `code`, `em`, `i`, `mark`, `q`, `s`, `small`, `span`, `strong`, |`p`|

#### Arguments
`input()` and `print()` both support the `magic_args` keyword argument. `magic_args` accepts a dictionary, which can be used to set attributes for the html element.

### Cache
The user script is re-evaluated after each user interaction, to progress the script to the next `input()`, etc. This means expensive functions may be called more than once per session. To reduce latency, a cache decorator is made available through the `python_web_io` module. The `@cache_to_file()` decorator accepts a single argument: `file_path`, which indicates where the cache (a `.pkl` file) should be stored.

```python3
import python_web_io as io

@io.cache_to_file('cache.pickle')
def expensive_function(arg):
    # Calculate the result here
    return result
```

Cache is persistent across sessions, allowing multiple users to access it. Session specific data can be stored using `session` from `flask`.

```python3
from flask import session
session['some_var] = 'some_val'
```

Reserved keys for the `session` namespace are: `io` and `counter`. 

## License
MIT
