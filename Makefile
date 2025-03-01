.PHONY: env lint build start st

env:
	@. .venv/bin/activate
	@poetry env list

lint:
	@ruff check
	@black --line-length 79 .

build:
	@docker compose build

start:
	@docker compose up --build -d

st:
	@streamlit run app/client.py
