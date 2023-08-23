---
permalink: /docs/config/
toc: true
title: Configuration and settings
---

The appearance of generated pages are customisable via a `config.toml` file.
Create a subdirectory `/.pythonwebio` relative to were the project will be called from, and create a `config.toml` file inside.
```
.
├── app.py
├── .envrc
└── .pythonwebio/
    └── config.toml
```

## Example `.envrc`

If using a `config.toml` file in a non-default location (and deploying via `uvicorn`), set the config filepath via the `PYTHON_WEB_IO_CONFIG` environment variable. 

```bash
# server env vars
export PYTHON_WEB_IO_SECRET=""
export PYTHON_WEB_IO_CONFIG=".pythonwebio/config.toml" 	# defaults to .pythonwebio/config.toml if not set
```

## Example `config.toml`

```TOML
[script]
filepath = "app.py"
entrypoint = "main"

[page]
name = "Python web I/O App"
icon = "🎯"
css = [
    "https://unpkg.com/normalize.css@8.0.1/normalize.css",
    "https://unpkg.com/simpledotcss/simple.min.css",
]

[about]
author = "Zachary"
profile = "https://github.com/Cutwell"
description = "Generate a webpage as a GUI for a Python script, and serve from anywhere."

[project]
homepage = "https://github.com/Cutwell/python-web-io"
license = "https://github.com/Cutwell/python-web-io/blob/main/LICENSE"
issues = "https://github.com/Cutwell/python-web-io/issues/new"

[server]
debug = false
```

## CLI

`python_web_io` is designed to be run (for production and development) using `uvicorn`. Use the [uvicorn settings](https://www.uvicorn.org/settings/) docs for a reference to setup your server.

For quick testing, `python_web_io` can also be ran as a Python script. Running directly spawns a `uvicorn` server with limited config options. Test mode is designed for evaluating multiple scripts quickly without editing a `config.toml` file, e.g.: testing the `/examples` scripts.

```bash
poetry run python_web_io --script="app.py" --config=".pythonwebio/config.toml" --host="localhost" --port=8000
```

|||
|:---:|:---|
|`--script`|Override `[script]` settings (format: `<filepath>:<entrypoint>`, e.g.: `app.py:main`) (default: None).|
|`--config`|Override the `PYTHON_WEB_IO_CONFIG` environment variable and default `.pythonwebio/config.toml` config filepaths (default: `.pythonwebio/config.toml`).|
|`--host`|Set the Uvicorn server host (default: `localhost`).|
|`--port`|Set the Uvicorn server port (default: `8000`).|

## `config.toml` Documentation

### `[script]`

|||
|:---:|:---|
|`filepath`|Rather than provide a script filepath via command line, an app filepath can also be defined here.|
|`entrypoint`|Python scripts using the typical `if __name__ == '__main__': main()` will not run, as this check will fail. To resolve this, a function name can be supplied as an entrypoint for the script, and will be called to begin execution.|

### `[page]`

|||
|:---:|:---|
|`name`|Webapp name, used as the website / tab title.|
|`icon`|Webapp icon, used in bookmarks and in the tab.|
|`css`|Drop-in CSS styling is supported and encouraged to customise a web-app to user preference. A curated list of drop-in stylesheets can be found [here](https://github.com/sw-yx/spark-joy/blob/master/README.md#drop-in-css-frameworks). This option can be a list of stylesheets or a single item.|

### `[about]`

These options populate the `About` modal, accessible from the page footer.

|||
|:---:|:---|
|`author`|Author's name / online alias.|
|`profile`|Author social link, e,g.: GitHub, Twitter, etc.|
|`description`|A short description to summarise the webapp.|

### `[project]`

These options populate the `Help` modal, accessible from the page footer.

|||
|:---:|:---|
|`homepage`|A link to the project homepage, for instance on GitHub.|
|`license`|A link to the license the project is distributed under.|
|`issues`|A link to a forum / issue tracker for reporting bugs users may encounter.|

### `[server]`

These options are for the underlying FastAPI server:

|||
|:---:|:---|
|`debug`|Boolean to enable debug mode.|

---

Next steps:

1. Learn how to [serve static files](https://cutwell.github.io/python-web-io/docs/static/), such as images or CSS files.
2. Deep dive into customising your webpage using `print()` and `input()` [overrides](https://cutwell.github.io/python-web-io/docs/io/).