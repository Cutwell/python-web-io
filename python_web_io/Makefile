IMAGE_NAME = python_web_io
EXAMPLE_PY = tests/colors_example.py

dev: # run example.py using local development version
	@poetry run $(IMAGE_NAME) $(EXAMPLE_PY)

publish:
	@poetry build
	@poetry publish
