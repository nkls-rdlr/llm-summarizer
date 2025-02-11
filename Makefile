.PHONY: venv build start streamlit

venv:
	@. .venv/bin/activate
	@poetry env list

build:
	@docker compose build

start:
	@docker compose up --build -d

streamlit:
	@streamlit run app/client.py
