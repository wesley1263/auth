.PHONY: build start stop clean test logs help

help:
	@echo "Available commands:"
	@echo "  make dev  - Run application locally with autoreload"
	@echo "  make build  - Build Docker containers"
	@echo "  make start  - Start the application"
	@echo "  make stop   - Stop the application"
	@echo "  make clean  - Remove containers and volumes"
	@echo "  make test   - Run tests"
	@echo "  make logs   - Display application logs"

dev:
	@uvicorn main:app --reload
	
build:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down -v

test:
	docker-compose run --rm app pytest

logs:
	docker-compose logs -f

clear:
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	
lint:
	poetry run black .
	poetry run isort .
	poetry run flake8
	poetry run autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive .

setup-dev:
	poetry install --with dev
	pre-commit install

.DEFAULT_GOAL := help