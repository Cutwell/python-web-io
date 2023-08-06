CONFIG = examples/weather_app.toml

dev: ## run example config
	@poetry run python_web_io --config=$(CONFIG)

debug: ## run example config locally with Flask server debug enabled
	@poetry run python_web_io --config=$(CONFIG) --debug

install: ## install dependencies
	@poetry config virtualenvs.in-project true; poetry install

publish: ## build module and publish as new version to PyPI
	@poetry build
	@poetry publish

help: ## display this help screen
    @grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'