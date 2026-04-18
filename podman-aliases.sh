#!/bin/bash
# podman-aliases.sh - Aliases para facilitar uso de Podman
# Source este arquivo: source podman-aliases.sh

# Detectar se Podman está disponível
if command -v podman &> /dev/null; then
    echo "🐳 Podman detectado - criando aliases..."

    # Criar aliases Docker→Podman
    alias docker='podman'
    alias docker-compose='podman-compose'

    # Exportar para subshells
    export DOCKER_CMD=podman
    export DOCKER_COMPOSE_CMD=podman-compose

    echo "✅ Aliases criados:"
    echo "  docker → podman"
    echo "  docker-compose → podman-compose"
    echo ""
    echo "💡 Use comandos 'docker' normalmente, eles usarão Podman!"

else
    echo "⚠️  Podman não encontrado, usando Docker se disponível"
fi
