# Dockerfile otimizado para web2md + Test Automation
# Multi-stage build para imagem final pequena e eficiente

# ========================================
# STAGE 1: Builder
# ========================================
FROM python:3.14-slim AS builder

# Instalar dependências de build
RUN apt-get update -qq && \
    apt-get install -y -qq \
        curl \
        git \
        gcc \
        g++ \
        make \
    && rm -rf /var/lib/apt/lists/*

# Instalar Bun (para web2md)
RUN curl -fsSL https://bun.sh/install.sh | bash

# Copiar requirements
COPY tests/requirements.txt requirements.txt

# Instalar dependências Python
RUN pip install --user --no-cache-dir -r requirements.txt

# ========================================
# STAGE 2: Runtime
# ========================================
FROM python:3.14-slim

# Metadados
LABEL maintainer="lucascardoso"
LABEL description="web2md + Test Automation + Auto-Research"
LABEL version="1.0.0"

# Instalar dependências runtime
RUN apt-get update -qq && \
    apt-get install -y -qq \
        curl \
        git \
        jq \
        ripgrep \
        vim \
    && rm -rf /var/lib/apt/lists/*

# Instalar Bun (runtime)
RUN curl -fsSL https://bun.sh/install.sh | bash

# Copiar dependências Python do builder
COPY --from=builder /root/.local /root/.local

# Criar diretório de trabalho
WORKDIR /app

# Copiar código fonte
COPY . .

# Instalar web2md dependencies
RUN cd web2md && bun install

# Instalar dependências Python
RUN pip install --user --no-cache-dir -r requirements.txt

# Criar diretório para research
RUN mkdir -p /root/.claude/research/discovered

# Copiar scripts de teste
COPY tests/run-all-tests.sh /app/tests/
RUN chmod +x /app/tests/run-all-tests.sh

# ========================================
# STAGE 3: Test Runner
# ========================================
FROM python:3.14-slim AS test-runner

# Instalar dependências de teste
RUN pip install --user \
    behave \
    pytest \
    pytest-cov \
    locust \
    flake8 \
    mypy \
    bandit \
    safety \
    jinja2 \
    markupsafe

# Copiar código fonte
COPY --from=0 /app /app

WORKDIR /app

# Comandos padrão
CMD ["python", "-m", "behave", "tests/features/"]
