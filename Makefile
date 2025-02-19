.PHONY: env lint test app

env:
	@. .venv/bin/activate
	@poetry env list

lint:
	@poetry run ruff check
	@poetry run black --line-length 79 .
	@poetry run mypy .

test:
	@poetry run pytest .

app:
	@poetry run streamlit run app/client.py
