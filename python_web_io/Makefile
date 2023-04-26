IMAGE_NAME = python_web_io
EXAMPLE_PY = tests/colors_example.py

dev: # run test script locall
	@poetry run $(IMAGE_NAME) $(EXAMPLE_PY)

debug: # run test script locally with Flask server debug enabled
	@poetry run $(IMAGE_NAME) $(EXAMPLE_PY) --debug

publish:
	@poetry build
	@poetry publish
