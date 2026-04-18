# 🔄 GitLab CI/CD - Docker Integration

Pipeline completo GitLab CI integrado com Docker para testes automatizados.

## ✅ Configuração Completa

### 1. GitLab CI com Docker

**Arquivo:** `.gitlab-ci.yml`

**6 Stages:**
1. **discover** - Auto-research de ferramentas
2. **build** - Build Docker images
3. **test** - BDD + TDD em containers
4. **performance** - Locust load tests
5. **quality** - Flake8, Mypy, Bandit
6. **report** - Relatório consolidado

### 2. Integração Docker

```yaml
build:image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $WEB2MD_IMAGE .
    - docker push $WEB2MD_IMAGE

test:bdd:
  stage: test
  image: $WEB2MD_IMAGE-test
  script:
    - behave tests/features/
```

### 3. Variáveis GitLab

**Necessárias configurar no GitLab:**

```bash
# GitLab → Settings → CI/CD → Variables
CI_REGISTRY_USER           # Seu usuário GitLab
CI_REGISTRY_PASSWORD       # GitLab Access Token
CI_REGISTRY                # registry.gitlab.com
CI_REGISTRY_IMAGE          # registry.gitlab.com/seu-usuario/web2md
```

## 🚀 Como Funciona

### Pipeline Automático

**Push para branch:**
```bash
git push origin main
```

**O que acontece:**
1. GitLab detecta novo commit
2. Dispara pipeline `.gitlab-ci.yml`
3. Build Docker images
4. Roda testes em containers
5. Gera relatórios
6. Salva artifacts

### Stages em Detalhe

#### Stage 1: Discover (Auto-Research)
```yaml
discover:
  stage: discover
  script:
    - bash ~/.claude/research/auto-research.sh
```

#### Stage 2: Build (Docker)
```yaml
build:image:
  stage: build
  script:
    - docker build -t $WEB2MD_IMAGE .
    - docker push $WEB2MD_IMAGE
```

#### Stage 3: Test (BDD + TDD)
```yaml
test:bdd:
  stage: test
  image: $WEB2MD_IMAGE-test
  script:
    - behave tests/features/

test:tdd:
  stage: test
  image: $WEB2MD_IMAGE-test
  script:
    - pytest tests/unit/ --cov=.
```

#### Stage 4: Performance (Locust)
```yaml
performance:
  stage: performance
  image: $WEB2MD_IMAGE-test
  script:
    - locust -f locustfile.py --headless --html performance.html
```

#### Stage 5: Quality (Gates)
```yaml
quality:flake8:
  stage: quality
  script:
    - flake8 . --max-line-length=100

quality:security:
  stage: quality
  script:
    - bandit -r . -f json -o bandit-report.json
```

#### Stage 6: Report (Consolidado)
```yaml
report:
  stage: report
  script:
    - python scripts/generate-report.py
  artifacts:
    paths:
      - reports/
```

## 🔧 Configuração

### 1. Criar Access Token

**GitLab:**
1. Settings → Access Tokens
2. Create token: `ci_registry`
3. Scopes: `read_registry`, `write_registry`
4. Copiar token

### 2. Configurar Variáveis

**GitLab → Settings → CI/CD → Variables:**

```bash
# Adicionar variáveis
CI_REGISTRY_USER = seu-usuario
CI_REGISTRY_PASSWORD = glpat-xxxxx (token criado)
```

### 3. Testar Localmente

```bash
# Testar build Docker localmente
make docker-build

# Testar script de testes
./tests/run-docker-tests.sh
```

### 4. Commit & Push

```bash
git add .
git commit -m "feat: Add GitLab CI with Docker"
git push origin main
```

## 📊 Pipeline em Ação

### Primeira Execução

1. **GitLab** detecta push
2. **Pipeline** inicia automaticamente
3. **Jobs** executam em paralelo
4. **Docker images** buildadas
5. **Testes** rodam em containers
6. **Relatórios** gerados

### Ver Pipeline

**GitLab:**
- CI/CD → Pipelines
- Clique no pipeline ID
- Veja jobs rodando
- Check logs

### Ver Relatórios

**Artifacts:**
- CI/CD → Pipelines → #ID
- Jobs → report → Browse
- Download `reports/`

## 🎯 Jobs Manuais

**Trigger sob demanda:**

```yaml
test:all:manual:
  stage: test
  when: manual
  script:
    - ./tests/run-all-tests.sh
```

**Como usar:**
1. GitLab → CI/CD → Pipelines
2. "Run pipeline" button
3. Selecionar jobs manuais
4. Execute

## 📈 Métricas

### Coverage
```yaml
coverage: '/Coverage: \d+\.\d+%//'
```

### Performance
```yaml
# Locust gera performance.html
locust -f locustfile.py --headless --html performance.html
```

### Security
```yaml
# Bandit gera bandit-report.json
bandit -r . -f json -o bandit-report.json
```

## 🔄 Workflow

### Merge Request

```bash
# Criar branch
git checkout -b feature/new-feature

# Fazer mudanças
git add .
git commit -m "feat: Add new feature"

# Push
git push origin feature/new-feature

# Criar MR no GitLab
# Pipeline roda automaticamente
```

### Main Branch

```bash
# Merge MR para main
# Pipeline roda novamente
# Docker images tagged como :latest
```

## 🐛 Troubleshooting

### Job Falha

**Ver logs:**
1. CI/CD → Pipelines → #ID
2. Job → Click para ver logs

**Comum erros:**
- `docker login` failed → Check `CI_REGISTRY_*` variables
- `docker build` failed → Check Dockerfile
- `pytest` failed → Check test code

### Docker-in-Docker

**Se jobs falham com Docker:**
```yaml
services:
  - docker:dind
variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
```

### Registry Issues

**Push falha:**
```bash
# Check credentials
echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin

# Check registry
docker pull $CI_REGISTRY_IMAGE:latest
```

## 📋 Checklist

**Antes do primeiro push:**
- [ ] Criar GitLab Access Token
- [ ] Configurar variáveis CI/CD
- [ ] Testar `docker build` localmente
- [ ] Testar `make docker-test`
- [ ] Commitar `.gitlab-ci.yml`
- [ ] Push e verificar pipeline

## 🚀 Benefits

1. **Automated** - Testes rodam automaticamente
2. **Docker** - Ambiente consistente
3. **Parallel** - Jobs rodam em paralelo
4. **Artifacts** - Relatórios salvos
5. **Manual** - Jobs on-demand
6. **Security** - Scans automatizados

## 🎉 Pronto!

**Pipeline configurado e integrado com Docker!**

```bash
# Teste agora
git push origin main

# Veja o pipeline
# GitLab → CI/CD → Pipelines
```

---

**Baseado em:** GitLab CI + Docker Multi-stage + Behave/Pytest/Locust
**Próxima atualização:** Quando adicionar novos testes
