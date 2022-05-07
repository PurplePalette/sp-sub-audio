start:
	poetry run uvicorn src.main:app --reload

lint:
	poetry run pysen run lint

lint-fix:
	poetry run pysen run format && \
	poetry run pysen run lint

test-unit:
	poetry run pytest

install-dev:
	poetry install

install:
	poetry install --no-dev
