install:
	poetry install

reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

build:
	poetry build

lint:
	poetry run flake8 page_loader tests

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml