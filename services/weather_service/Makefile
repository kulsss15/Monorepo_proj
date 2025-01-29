.PHONY: install dev lint test build run

install:
	poetry install

dev:
	poetry run uvicorn src.weather_service.main:app --reload

prod:
	poetry run uvicorn src.weather_service.main:app --reload

lint:
	poetry run pylint src/

test:
	poetry run pytest

build:
	docker build -t weather_service .

run:
	docker run -d --name weather_service_container -p 8002:8002 weather_service
