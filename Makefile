.PHONY: run dev docker-build docker-run test

run:
    uvicorn app.main:app --host 0.0.0.0 --port 8080

dev:
    APP_ENV=local uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

docker-build:
    docker build -t fastapi-starter:latest .

docker-run:
    docker run -p 8080:8080 -e APP_ENV=docker fastapi-starter:latest

test:
    pytest -q