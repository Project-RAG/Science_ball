.PHONY: help up down build logs ps clean test

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

build: ## Build backend and worker images
	docker compose build

logs: ## Tail logs for all services
	docker compose logs -f

ps: ## Show running services
	docker compose ps

clean: ## Stop services and remove volumes
	docker compose down -v

test: ## Run backend tests
	cd backend && python -m pytest

config: ## Validate docker compose config
	docker compose config

infra-up: ## Start only infrastructure (no backend/worker)
	docker compose up -d postgres redis elasticsearch neo4j minio

infra-down: ## Stop infrastructure
	docker compose stop postgres redis elasticsearch neo4j minio
