# 🤝 Contributing to web2md

## 🚀 Como Contribuir

### Setup do Ambiente

```bash
# Clonar repositório
git clone <repo-url>
cd web2md

# Instalar dependências
pip install -r requirements-dev.txt

# Instalar web2md globalmente
./install.sh
```

### Desenvolvimento

```bash
# Rodar testes
make test-all

# Formatar código
black .
isort .

# Type check
mypy .
```

### Estrutura

```
web2md/
├── web2md.ts              # Core (Bun)
├── scripts/              # Scripts Python
├── tests/                # Testes
│   ├── features/         # BDD
│   ├── steps/            # Step definitions
│   └── pages/            # Page Objects
└── docs/                 # Documentação
```

### Commit

```bash
# Seguir padrão de commits
git checkout -b feature/nova-feature
git commit -m "feat: add nova feature"
git push origin feature/nova-feature
```

## 📋 Padrões

### Código
- **TypeScript**: 2 espaços, single quotes
- **Python**: 2 espaços, type hints
- **Markdown**: 80 chars por linha

### Commits
- `feat:` nova feature
- `fix:` bug fix
- `docs:` documentação
- `test:` testes
- `refactor:` refatoração

## 🧪 Testes

```bash
# Unit tests
pytest tests/unit/ -v

# BDD tests
behave tests/features/

# Performance
locust -f locustfile.py --headless
```

## 📚 Mais Info

- [README.md](README.md)
- [CHANGELOG.md](CHANGELOG.md)
- [GITLAB.md](GITLAB.md)
