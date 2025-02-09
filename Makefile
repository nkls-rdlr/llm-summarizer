.PHONY: venv build start

venv:
	@. .venv/bin/activate
	@poetry env list

build:
	@docker compose build

start:
	@docker compose up --build -d
