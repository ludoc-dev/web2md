# 🐳 Podman Support - web2md

Podman é 100% compatível com Docker, mas mais seguro (sem daemon, rootless).

## ✅ Compatibilidade

**Sim, funciona com Podman!** Todos os comandos Docker funcionam com Podman:

```bash
# Substituir 'docker' por 'podman'
podman build -t web2md .
podman run -it web2md
podman-compose up -d
```

## 🔄 Podman vs Docker

| Característica | Docker | Podman |
|----------------|--------|--------|
| Daemon | ✅ Sim | ❌ Não (rootless) |
| Root required | ✅ Sim | ❌ Não |
| Security | ⚠️ Medium | ✅ High |
| Compatibilidade | - | ✅ 100% Docker API |
| Comandos | docker | podman |

## 🚀 Usando Podman

### 1. Instalar Podman

```bash
# macOS
brew install podman

# Linux (Ubuntu/Debian)
sudo apt install podman

# Inicializar
podman machine init
podman machine start
```

### 2. Podman Compose

```bash
# Instalar podman-compose (Python)
pip install podman-compose

# Ou usar docker-compose com Podman
# Podman emula Docker API
```

### 3. Substituir Comandos

```bash
# Docker → Podman
docker build → podman build
docker run → podman run
docker-compose → podman-compose
```

## 📦 Arquivos Adaptados

### Makefile com Podman

```makefile
# Detectar automaticamente
DOCKER ?= $(shell command -v podman >/dev/null 2>&1 && echo podman || echo docker)
DOCKER_COMPOSE ?= $(shell command -v podman-compose >/dev/null 2>&1 && echo podman-compose || echo docker-compose)

# Usar variável
docker-build:
	$(DOCKER) build -t web2md .
```

### Scripts Adaptados

```bash
# Auto-detecta Docker ou Podman
CONTAINER_CMD=""
if command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
elif command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
else
    echo "❌ Nem Docker nem Podman encontrado"
    exit 1
fi

echo "🐳 Usando: $CONTAINER_CMD"
```

## 🎯 Vantagens Podman

1. **Segurança:** Rootless por padrão
2. **Sem daemon:** Menos superfície de ataque
3. **Compatível:** 100% Docker API
4. **Pods:** Nativos (como Kubernetes)
5. **Systemd integration:** Melhor que Docker

## 🚀 Quick Start Podman

```bash
# 1. Inicializar Podman machine
podman machine init
podman machine start

# 2. Build
podman build -t web2md .

# 3. Run
podman run -it web2md

# 4. Compose
podman-compose up -d
```

## 📋 Suporte no Projeto

O projeto suporta **ambos** automaticamente:

- ✅ Makefile detecta e usa o disponível
- ✅ Scripts funcionam com ambos
- ✅ Dockerfile 100% compatível
- ✅ docker-compose.yml funciona

---

**Use Docker ou Podman - sua escolha!**
