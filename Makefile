APP_NAME = delivery-optimizer
PORT = 8000

.PHONY: help
help:
	@echo "Usage:"
	@echo "	make run			Run the FastAPI app using Uvicorn"
	@echo "	make dev 			Run app in auto-reload dev mode"
	@echo "	make build			Build Docker image"
	@echo "	make docker-run			Run app via Docker"
	@echo "	make lint			Lint code using flake8"
	@echo "	make format			Format code using black"
	@echo "	make test			Run unit tests"
	@echo "	make clean			Clean up Python caches and Docker image/container"

.PHONY: run
run:
	uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

.PHONY: dev
dev:
	uvicorn app.main:app --reload --port $(PORT)

.PHONY: build
build:
	docker build -t $(APP_NAME) .

.PHONY: docker-run
docker-run:
	docker run -p $(PORT):800 $(APP_NAME)

.PHONY: lint
lint:
	flake8 app

.PHONY: format
format:
	black app tests

.PHONY: test
test:
	pytest

.PHONY: clean
clean:
	@echo "Removing __pycache__ and .pyc files..."
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -exec rm -r {} + 2>/dev/null || true

	@echo "Removing Docker containers created from image..."
	docker ps -a --filter "ancestor=$(APP_NAME)" --format '{{.ID}}' | xargs -r docker rm -f 

	@echo "Removing Docker image $(APP_NAME)..."
	docker images --filter=reference=$(APP_NAME) --format '{{.ID}}' | xargs -r docker rmi -f