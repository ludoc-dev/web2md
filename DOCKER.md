# 🐳 Docker - web2md

Ambiente Docker completo para desenvolvimento, testes e CI/CD.

## 📋 Estrutura Docker

```
web2md/
├── Dockerfile              # Multi-stage build (3 stages)
├── docker-compose.yml      # Orquestração desenvolvimento
├── docker-compose.test.yml # Orquestração testes
├── Makefile                # Comandos facilitados
└── tests/
    ├── run-docker-tests.sh # Script testes Docker
    └── run-all-tests.sh    # Script testes locais
```

## 🚀 Quick Start

### 1. Build Images

```bash
make docker-build
# ou
docker-compose build
```

### 2. Start Containers

```bash
make docker-up
# ou
docker-compose up -d
```

### 3. Run Tests

```bash
make docker-test
# ou
./tests/run-docker-tests.sh
```

### 4. Stop Containers

```bash
make docker-down
# ou
docker-compose down
```

## 📦 Docker Stages

### Stage 1: Builder

**Propósito:** Compilar dependências

```dockerfile
FROM python:3.14-slim AS builder
- Instala Bun
- Compila dependências Python
- Otimiza para cache
```

### Stage 2: Runtime

**Propósito:** Ambiente de produção

```dockerfile
FROM python:3.14-slim
- Python + Bun runtime
- web2md instalado
- Scripts de pesquisa
```

### Stage 3: Test Runner

**Propósito:** Ambiente de testes

```dockerfile
FROM python:3.14-slim AS test-runner
- Behave (BDD)
- Pytest (TDD)
- Locust (Performance)
- Flake8, Mypy, Bandit (Quality)
```

## 🎯 Serviços Docker Compose

### web2md (Principal)

```yaml
web2md:
  build:
    target: runtime
  volumes:
    - .:/app
    - ~/.claude/research:/root/.claude/research
  environment:
    - PYTHONUNBUFFERED=1
  command: tail -f /dev/null
```

**Uso:**
```bash
# Executar web2md
docker exec -it web2md bun run web2md.ts https://example.com

# Shell interativo
docker exec -it web2md bash
```

### test-runner

```yaml
test-runner:
  build:
    target: test-runner
  volumes:
    - .:/app
    - ./reports:/app/reports
  depends_on:
    - web2md
```

**Uso:**
```bash
# Rodar BDD tests
docker exec test-runner behave tests/features/

# Rodar TDD tests
docker exec test-runner pytest tests/unit/ -v

# Shell interativo
docker exec -it test-runner bash
```

### locust-ui

```yaml
locust-ui:
  image: locustio/locust
  ports:
    - "8089:8089"
  volumes:
    - ./locustfile.py:/mnt/locustfile.py
```

**Uso:**
```bash
# Acessar UI
open http://localhost:8089

# Rodar em modo headless
docker exec locust locust --locustfile /mnt/locustfile.py --headless \
  --users 10 --run-time 30s --host https://example.com
```

### gitlab-runner

```yaml
gitlab-runner:
  image: gitlab/gitlab-runner:latest
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
  privileged: true
```

**Registro:**
```bash
docker exec -it gitlab-runner gitlab-runner register \
  --url https://gitlab.com \
  --registration-token <TOKEN> \
  --executor docker \
  --docker-privileged
```

## 🧪 Testes em Docker

### Script Completo

```bash
./tests/run-docker-tests.sh
```

**O que roda:**
1. Build das images
2. Start containers
3. Unit tests (Pytest)
4. BDD tests (Behave)
5. Performance tests (Locust)
6. Code quality (Flake8, Bandit)
7. Coverage reports
8. Cleanup

### Testes Individuais

```bash
# BDD
docker exec test-runner behave tests/features/

# TDD
docker exec test-runner pytest tests/unit/ -v

# Performance
docker exec locust locust --locustfile /mnt/locustfile.py --headless \
  --users 10 --run-time 10s --host https://example.com

# Quality
docker exec test-runner flake8 . --exclude=node_modules
docker exec test-runner bandit -r . -f json -o reports/bandit-report.json
```

## 📊 Makefile Commands

### Desenvolvimento

```bash
make help              # Mostra todos os comandos
make dev-install       # Instala dependências
make dev-check         # Verifica ambiente
```

### Testes Locais

```bash
make test              # Todos os testes
make test-bdd          # Apenas BDD
make test-tdd          # Apenas TDD
make test-performance  # Apenas performance
make test-quality      # Apenas quality checks
```

### Docker

```bash
make docker-build      # Build images
make docker-up         # Sobe containers
make docker-down       # Para containers
make docker-test       # Testes em Docker
make docker-logs       # Mostra logs
make docker-shell      # Shell no test-runner
make docker-web2md     # Shell no web2md
```

### Limpeza

```bash
make clean             # Limpa artefatos locais
make clean-docker      # Limpa containers+volumes
make clean-all         # Limpa tudo
```

### Coverage

```bash
make coverage          # Gera relatório
make coverage-open     # Abre no browser
```

### web2md

```bash
make web2md URL=https://example.com
make web2md-file URL=https://example.com OUT=output.md
```

## 🔧 Troubleshooting

### Container não starta

```bash
# Ver logs
docker-compose logs web2md

# Ver status
docker ps -a

# Rebuild
docker-compose build --no-cache
```

### Permissões negadas

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Relogin necessário
```

### Portas em uso

```bash
# Ver processos nas portas
lsof -i :8089
lsof -i :3000

# Mudar portas no docker-compose.yml
```

### Volumes persistindo

```bash
# Limpar volumes
docker-compose down -v

# Limpar tudo
docker system prune -a --volumes
```

## 📈 Performance Docker

### Otimizações

1. **Multi-stage build** - Imagem final pequena
2. **Cache de dependências** - Builds rápidos
3. **Volumes para código** - Hot reload
4. **Paralelismo** - Containers independentes

### Tamanhos

| Stage | Tamanho | Uso |
|-------|---------|-----|
| builder | ~500MB | Build |
| runtime | ~200MB | Produção |
| test-runner | ~300MB | Testes |

## 🔄 CI/CD Integration

### GitLab CI

```yaml
test-docker:
  stage: test
  script:
    - docker-compose build
    - ./tests/run-docker-tests.sh
  only:
    - merge_requests
    - master
```

### Local Pipeline

```bash
# Simular pipeline completo
make docker-build
make docker-test
make docker-down
```

## 💡 Tips

### Desenvolvimento Rápido

```bash
# 1. Start containers
make docker-up

# 2. Shell no test-runner
make docker-shell

# 3. Rodar testes iterativamente
behave tests/features/
pytest tests/unit/ -v

# 4. Cleanup
make docker-down
```

### Debug

```bash
# Ver logs em tempo real
docker-compose logs -f

# Entrar no container
docker exec -it test-runner bash

# Ver variáveis de ambiente
docker exec test-runner env
```

### Hot Reload

```bash
# Código montado via volume
# Alterações refletem automaticamente

# Verificar
docker exec test-runner ls -la /app
```

## 🎯 Próximos Passos

1. **Build:** `make docker-build`
2. **Test:** `make docker-test`
3. **Develop:** `make docker-up && make docker-shell`
4. **Deploy:** `docker push registry/web2md:latest`

---

**Baseado em:** Multi-stage builds + Docker Compose + Make
**Próxima atualização:** Quando adicionar novos serviços
