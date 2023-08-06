dev: ## run locally
	@poetry run uvicorn python_web_io.main:app --reload --port=8000

install: ## install dependencies
	@poetry config virtualenvs.in-project true; poetry install

publish: ## build module and publish as new version to PyPI
	@poetry build
	@poetry publish

help: ## display this help screen
    @grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'