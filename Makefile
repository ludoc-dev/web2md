# Makefile - web2md Test Automation
# Facilita execução de testes e comandos Docker

.PHONY: help test test-bdd test-tdd test-performance test-quality test-all docker-test docker-build docker-up docker-down clean

# Variáveis
PROJECT_NAME := web2md

# Auto-detectar Podman ou Docker
CONTAINER_ENGINE := $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)
ifeq ($(CONTAINER_ENGINE),podman)
    DOCKER_COMPOSE := podman-compose
else
    DOCKER_COMPOSE := docker-compose
endif
DOCKER_COMPOSE_TEST := $(DOCKER_COMPOSE) -f docker-compose.test.yml

# ========================================
# HELP
# ========================================
help: ## Mostra este help
	@echo "📋 $(PROJECT_NAME) - Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ========================================
# TESTS LOCAIS
# ========================================
test: test-all ## Roda todos os testes localmente

test-bdd: ## Roda apenas BDD tests (Behave)
	@echo "🎭 Rodando BDD tests..."
	behave tests/features/ -f pretty

test-tdd: ## Roda apenas TDD tests (Pytest)
	@echo "🔬 Rodando TDD tests..."
	pytest tests/unit/ -v --tb=short

test-performance: ## Roda apenas Performance tests (Locust)
	@echo "⚡ Rodando Performance tests..."
	locust -f locustfile.py --headless --users 10 --run-time 10s --host https://example.com

test-quality: ## Roda apenas Code Quality checks
	@echo "🔍 Rodando Code Quality checks..."
	flake8 . --exclude=node_modules,dist,build,.eggs --max-line-length=100
	bandit -r . -f json -o reports/bandit-report.json

test-all: ## Roda todos os testes localmente
	@echo "🧪 Rodando todos os testes..."
	./tests/run-all-tests.sh

# ========================================
# DOCKER
# ========================================
docker-build: ## Build Docker/Podman images
	@echo "🔨 Building images with $(CONTAINER_ENGINE)..."
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE_TEST) build

docker-up: ## Sobe containers (Docker/Podman)
	@echo "🚀 Starting containers with $(CONTAINER_ENGINE)..."
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE_TEST) up -d

docker-down: ## Para containers (Docker/Podman)
	@echo "🛑 Stopping containers..."
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE_TEST) down

docker-logs: ## Mostra logs dos containers
	$(DOCKER_COMPOSE) logs -f

docker-test: ## Roda testes em containers (Docker/Podman)
	@echo "🐳 Rodando testes com $(CONTAINER_ENGINE)..."
	./tests/run-docker-tests.sh

docker-shell: ## Abre shell no container test-runner
	docker exec -it test-runner bash

docker-web2md: ## Abre shell no container web2md
	docker exec -it web2md bash

# ========================================
# LIMPEZA
# ========================================
clean: ## Limpa artefatos de build e testes
	@echo "🧹 Limpando..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf reports/ || true

clean-docker: ## Limpa containers, volumes e images (Docker/Podman)
	@echo "🧹 Limpando com $(CONTAINER_ENGINE)..."
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE_TEST) down -v
	$(CONTAINER_ENGINE) system prune -f

clean-all: clean clean-docker ## Limpa tudo (local + Docker)

# ========================================
# DESENVOLVIMENTO
# ========================================
dev-install: ## Instala dependências de desenvolvimento
	@echo "📦 Installing dependencies..."
	pip install -r tests/requirements.txt
	bun install

dev-check: ## Verifica ambiente de desenvolvimento
	@echo "🔍 Checking environment..."
	@command -v python3 >/dev/null 2>&1 || echo "❌ Python 3 not found"
	@command -v bun >/dev/null 2>&1 || echo "❌ Bun not found"
	@echo "🐳 Container Engine:"
	@command -v podman >/dev/null 2>&1 && echo "  ✅ Podman found" || echo "  ⚠️  Podman not found"
	@command -v docker >/dev/null 2>&1 && echo "  ✅ Docker found" || echo "  ⚠️  Docker not found"
	@command -v $(DOCKER_COMPOSE) >/dev/null 2>&1 || echo "❌ $(DOCKER_COMPOSE) not found"
	@echo "✅ Environment check complete"

# ========================================
# COVERAGE
# ========================================
coverage: ## Gera relatório de coverage
	@echo "📊 Generating coverage report..."
	pytest tests/unit/ --cov=. --cov-report=html --cov-report=term
	@echo "📂 Coverage report: htmlcov/index.html"

coverage-open: coverage ## Abre relatório de coverage no browser
	@if command -v open >/dev/null 2>&1; then \
		open htmlcov/index.html; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open htmlcov/index.html; \
	else \
		echo "❌ Cannot open browser automatically"; \
	fi

# ========================================
# WEB2MD
# ========================================
web2md: ## Executa web2md (ex: make web2md URL=https://example.com)
	@if [ -z "$(URL)" ]; then \
		echo "❌ URL parameter required"; \
		echo "Usage: make web2md URL=https://example.com"; \
		exit 1; \
	fi
	bun run web2md.ts $(URL)

web2md-file: ## Executa web2md salvando em arquivo (ex: make web2md-file URL=https://example.com OUT=output.md)
	@if [ -z "$(URL)" ] || [ -z "$(OUT)" ]; then \
		echo "❌ URL and OUT parameters required"; \
		echo "Usage: make web2md-file URL=https://example.com OUT=output.md"; \
		exit 1; \
	fi
	bun run web2md.ts $(URL) --out $(OUT)

# ========================================
# DEFAULT
# ========================================
.DEFAULT_GOAL := help
