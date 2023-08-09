---
permalink: /docs/quickstart/
toc: true
---

After installing the project, some environment setup is required:

## Required setup

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
export PYTHON_WEB_IO_CONFIG="config.toml" 	# defaults to .pythonwebio/config.toml if not set
```

Generate a random key for `PYTHON_WEB_IO_SECRET` using this python command line snippet:
```bash
python -c 'import secrets; print(secrets.token_hex())'
```

If testing `wikipedia_assistant.py`, an OpenAI API key will also need to be set.
```bash
export OPENAI_API_KEY=""
```

## Running the webapp
We recommend running `python_web_io` using `uvicorn`:
```bash
poetry run uvicorn python_web_io.main:app
```