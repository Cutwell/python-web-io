# Examples

Setup the console to run an example app using:
```bash
cd python_web_io
poetry shell
```

## 🗺️ Global Weather Webapp
A weather app using [Open Meteo](https://open-meteo.com/) data. The city selection menu (selecting continent > country > city) works by using incremental CSS to hide series of button inputs.

```bash
poetry run python_web_io --config=examples/weather_app.toml
```

### Prerequisites:
Download the free [World Cities Database](https://simplemaps.com/data/world-cities). Un-zip the file and place `worldcities.csv` into this directory.

## 🤖 Linux GPT
Demo of LangChain integration, using an OpenAI LLM to imitate a linux terminal.

```bash
poetry run python_web_io --config=examples/linux_gpt.toml
```

## 🎨 Color names
A visually simple app that names user-selected colors based on their proximity to known named colors.

```bash
poetry run python_web_io --config=examples/color_names.toml
```