#!/bin/bash
# install-local.sh - Instala web2md para usuário atual

set -e

INSTALL_DIR="$HOME/web2md"
BIN_DIR="$HOME/.local/bin"

echo "📦 Instalando web2md para usuário atual..."

# Criar diretório bin
mkdir -p "$BIN_DIR"

# Criar link simbólico
ln -sf "$INSTALL_DIR/web2md-cli" "$BIN_DIR/web2md"

# Adicionar ao PATH se necessário
if [[ ":$BIN_DIR:" != *"$BIN_DIR"* ]]; then
    echo ""
    echo "⚠️  Adicione ao seu PATH:"
    echo ""
    echo "  export PATH=\"\$BIN_DIR:\$PATH\""
    echo ""
    echo "Adicione ao seu ~/.bashrc ou ~/.zshrc:"
    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""
fi

# Testar
echo "🧪 Testando instalação..."
export PATH="$BIN_DIR:$PATH"
web2md --version

echo ""
echo "✅ Instalação completa!"
echo ""
echo "Use: web2md <URL>"
