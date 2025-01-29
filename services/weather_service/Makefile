.PHONY: install dev lint test build run

install:
	poetry install

dev:
	poetry run uvicorn src.weather_service.main:app --reload

lint:
	poetry run pylint src/

test:
	poetry run pytest

build:
	docker build -t weather_service .

run:
	docker run -p 8001:8001 weather_service
