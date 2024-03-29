# <img src="https://raw.githubusercontent.com/Cutwell/python-web-io/main/.github/logo-40x38.png" style="width:40px;padding-right:10px;margin-bottom:-8px;" alt="Sticker of a cute yellow Python snake, representing the use of the Python programming language in this project."> Python Web I/O
 Generate a webpage as a GUI for a Python script, and serve from anywhere.

## Documentation
Check out the [wiki](https://cutwell.github.io/python-web-io/).

## Quickstart

Install `python-web-io` locally using:
```bash
pip install python-web-io
```

Or via `poetry` using:
```bash
poetry add python_web_io
```

If evaluating / testing `python-web-io`, install dependencies for the example apps using:
```bash
poetry add python_web_io --with examples
```

After installing the project, some environment setup is required:

### Required setup
Create an `app.py` file containing your script, a `config.toml` setting the script filepath and entrypoint, and an `.envrc` file to store project secrets. (Note: remember to add `.envrc` to your `.gitignore`). Look for example apps in [`/examples`](https://github.com/Cutwell/python-web-io/tree/main/python-web-io/examples).
```
.
├── .envrc
├── config.toml
└── app.py
```

Create the following simple `config.toml`:
```toml
[script]
filepath = "app.py"
entrypoint = "main"	# if your app has no entrypoint, remove this parameter.
```

Add the following environment variables to your `.envrc`. (Note: remember to activate the `.envrc` in your terminal using `direnv allow`)
```bash
# server env vars
export PYTHON_WEB_IO_SECRET=""
export PYTHON_WEB_IO_CONFIG=".pythonwebio/config.toml" 	# defaults to .pythonwebio/config.toml if not set
```

Generate a random key for `PYTHON_WEB_IO_SECRET` using this python command line snippet:
```bash
python -c 'import secrets; print(secrets.token_hex())'
```

If testing `wikipedia_assistant.py`, an OpenAI API key will also need to be set.
```bash
export OPENAI_API_KEY=""
```

### Running the webapp
We recommend running `python_web_io` using `uvicorn`:
```bash
poetry run uvicorn python_web_io.main:app
```

## License
MIT
