install:
	python3 -m venv .
	bin/pip install -e .

test:
	python3 -m venv .
	bin/pip install -e .[test]
	bin/pytest -x tests
