.PHONY: install dev build run clean test

install:
	poetry install

dev:
	poetry run uvicorn services.ai_service.src.ai_service.ml_main:app --reload
	poetry run uvicorn services.weather_service.src.weather_service.main:app --reload

build:
	docker-compose build

run:
	docker-compose up

test:
	pytest tests/

clean:
	rm -rf .venv
