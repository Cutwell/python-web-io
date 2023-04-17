# Python Web I/O
 Generate a webpage as a GUI for a Python script, and serve from anywhere.

## Usage
```
$ export FLASK_SECRET_KEY="someSecureSecretKey"
$ python_web_io .\example.py
```
* Create a `.envrc` file, setting `FLASK_SECRET_KEY` as per [`python_web_io/.envrc.example`](https://github.com/Cutwell/python-web-io/blob/main/python_web_io/.envrc.example).
* Try running the [`example.py`](https://github.com/Cutwell/python-web-io/blob/main/python_web_io/example.py) script using `python_web_io example.py`.

## Config
|Argument|||
|:---:|:---:|:---:|
|`"example.py"`|Required|Specify the file path for the app Python script / entrypoint.|
|`--title "Python Web I/O"`|Optional|Set a title for the browser tab / website title.|
|`--icon "🎯"`|Optional|Set an emoji icon for the browser tab / website icon.|
|`--debug`|Optional|Run the Flask server with debug output enabled.|

### Magic
`input()` and `print()` both support the `magic` keyword argument. For `input()`, `magic` sets the `type` of the input html element. For `print()`, `magic` sets the element type.

||Magic|Default|
|:---:|:---:|:---:|
|`input()`|`button`, `checkbox`, `color`, `date`, `datetime-local`, `email`, `file`, `image`, `month`, `number`, `password`, `radio`, `range`, `search`, `tel`, `text`, `time`, `url`, `week`|`text`|
|`print()`|`address`, `footer`, `aside`, `header`, `h1..6`, `blockquote`, `p`, `b`, `abbr`, `code`, `em`, `i`, `mark`, `q`, `s`, `small`, `span`, `strong`, |`p`|

#### Arguments
`input()` and `print()` both support the `magic_args` keyword argument. `magic_args` accepts a dictionary, which can be used to set attributes for the html element.

## License
MIT
