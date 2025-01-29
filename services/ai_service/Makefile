.PHONY: install dev lint test build run

install:
	poetry install

dev:
	poetry run uvicorn src.ai_service.ml_main:app --reload

lint:
	poetry run pylint src/

test:
	poetry run pytest

build:
	docker build -t ai_service .

run:
	docker run -p 8000:8000 ai_service
