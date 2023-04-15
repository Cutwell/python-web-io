# Python Web I/O
 Generate a webpage as a GUI for a Python script, and serve from anywhere.

## Getting started
1. Fork this repository.
2. Create a `.env` file in `/python_web_io` according to `/python_web_io/.env.example` (use any random if testing key).
3. Install poetry dependencies with `poetry install`.
4. Try running the `example.py` script using `poetry run python .\python_web_io\main.py .\example.py`. (Note: on Windows you may need to intialise poetry as a virtual environment, then try `python .\python_web_io\main.py .\example.py` from a terminal with the virtual environment activated)

## Config
|Argument|||
|:---:|:---:|:---:|
|`"example.py"`|Required|Specify the file path for the app Python script / entrypoint.|
|`--title "Python Web I/O"`|Optional|Set a title for the browser tab / website title.|
|`--icon "🎯"`|Optional|Set an emoji icon for the browser tab / website icon.|
|`--debug`|Optional|Run the Flask server with debug output enabled.|

## License
MIT
