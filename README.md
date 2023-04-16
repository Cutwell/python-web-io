# Python Web I/O
 Generate a webpage as a GUI for a Python script, and serve from anywhere.

## Install
```
$ pip install python-web-io
$ export FLASK_SECRET_KEY="someSecureSecretKey"
$ python_web_io .\example.py
```

## Getting started
1. Fork this repository.
From inside `/python_web_io`:
2. Create a `.envrc` file, setting `FLASK_SECRET_KEY` as per `python_web_io/.envrc.example`.
3. Install poetry dependencies with `poetry install`.
4. Try running the `example.py` script using `poetry run python python_web_io example.py`.

## Config
|Argument|||
|:---:|:---:|:---:|
|`"example.py"`|Required|Specify the file path for the app Python script / entrypoint.|
|`--title "Python Web I/O"`|Optional|Set a title for the browser tab / website title.|
|`--icon "🎯"`|Optional|Set an emoji icon for the browser tab / website icon.|
|`--debug`|Optional|Run the Flask server with debug output enabled.|

## License
MIT
