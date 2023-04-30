EXAMPLE_PY = tests/colors_example.py

dev: # run test script locall
	@poetry run python_web_io --script=$(EXAMPLE_PY)

debug: # run test script locally with Flask server debug enabled
	@poetry run python_web_io --script=$(EXAMPLE_PY) --debug

publish:
	@poetry build
	@poetry publish
