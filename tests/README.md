# 🧪 Test Suite - web2md

Testes completos BDD/TDD com critérios de aceitação baseados em pesquisa experimental.

## 📋 Estrutura de Testes

```
tests/
├── features/              # BDD scenarios (Behave)
│   ├── web2md-full.feature  # Cenários completos
│   └── environment.py       # Configuração Behave
├── steps/                # Step definitions
│   └── web2md_steps.py     # Implementação dos steps
├── unit/                 # TDD unit tests (Pytest)
│   └── test_web2md.py      # Testes unitários
├── acceptance/           # Critérios de aceitação
│   └── test-criteria.md    # Especificações
├── requirements.txt       # Dependências Python
├── pytest.ini            # Configuração Pytest
├── behave.ini            # Configuração Behave
├── locustfile.py         # Performance tests
└── run-all-tests.sh      # Executa todos os testes
```

## 🎯 Filosofia de Testes

### TDD (Test-Driven Development)

**Red, Green, Refactor:**

1. **Red** - Escrever teste falho primeiro
2. **Green** - Fazer teste passar
3. **Refactor** - Melhorar código

### BDD (Behavior-Driven Development)

**Cenários em linguagem natural:**

```gherkin
Dado que acesso uma URL de artigo
Quando executo web2md
Então devo receber Markdown limpo
E tempo de processamento < 5s
```

### Critérios de Aceitação

Baseados em pesquisa experimental com web2md:

- ✅ **90% economia de tokens** (15K → 1.5K tokens)
- ✅ **<5s para páginas simples**
- ✅ **Remoção de ruído** (ads, navbars, sidebars)
- ✅ **Preservação de estrutura** (headers, lists, code blocks)

## 🚀 Como Rodar os Testes

### Instalar Dependências

```bash
# Python dependencies
pip install -r tests/requirements.txt

# Bun (já deve estar instalado)
bun install
```

### Rodar Todos os Testes

```bash
# Executa tudo (BDD + TDD + Performance + Quality)
./tests/run-all-tests.sh
```

### Rodar Testes Individualmente

#### BDD Tests (Behave)

```bash
# Todos os cenários
behave tests/features/

# Cenários específicos
behave tests/features/web2md-full.feature

# Com tags
behave tests/features/ --tags=@critical
behave tests/features/ --tags=@P1
behave tests/features/ --tags=@javascript
```

#### TDD Tests (Pytest)

```bash
# Todos os unit tests
pytest tests/unit/ -v

# Com coverage
pytest tests/unit/ --cov=. --cov-report=html

# Testes específicos
pytest tests/unit/test_web2md.py::TestWeb2MDBasicExtraction -v

# Com marcadores
pytest tests/unit/ -m P1
pytest tests/unit/ -m critical
```

#### Performance Tests (Locust)

```bash
# Modo interativo (web UI)
locust -f locustfile.py

# Modo headless (CI/CD)
locust -f locustfile.py --headless --users 10 --run-time 30s --host https://example.com
```

## 📊 Matriz de Testes

### Prioridades

| Prioridade | Descrição           | Testes                              |
| ---------- | ------------------- | ----------------------------------- |
| **P1**     | Alta - Críticos     | Extração básica, ruído, performance |
| **P2**     | Média - Importantes | JavaScript, economia, estrutura     |
| **P3**     | Baixa - Opcionais   | Error handling, piping              |

### Categorias

| Categoria       | Tags            | Descrição                    |
| --------------- | --------------- | ---------------------------- |
| **Critical**    | @critical, @P1  | Testes de aceite críticos    |
| **JavaScript**  | @javascript     | Testes com --js flag         |
| **Economy**     | @economy        | Testes de economia de tokens |
| **Structure**   | @structure      | Testes de preservação        |
| **Performance** | @performance    | Testes de performance        |
| **Output**      | @output         | Testes de saída              |
| **Piping**      | @piping         | Testes de pipes              |
| **Error**       | @error_handling | Testes de erros              |

## 🎭 Cenários BDD

### Cenário 1: Extração Básica

```gherkin
@P1 @critical
Cenário: Extração de artigo simples
  Dado que acesso uma URL de artigo simples
  Quando executo web2md na URL
  Então devo receber Markdown limpo
  E tempo de processamento < 5s
  E economia de tokens > 85%
```

### Cenário 2: Remoção de Ruído

```gherkin
@P1 @critical
Cenário: Remoção de ruído
  Dado que acesso página com elementos de ruído
  Quando executo web2md
  Então Markdown não deve conter elementos de ruído
  E apenas conteúdo principal deve estar presente
```

### Cenário 3: Preservação de Estrutura

```gherkin
@P1 @critical
Cenário: Preservação de estrutura
  Dado que acesso página com formatação complexa
  Quando executo web2md
  Então Markdown deve ter estrutura equivalente
  E formatação deve ser válida
```

## 🔬 Testes Unitários (TDD)

### Exemplo de Teste

```python
def test_simple_extraction(self):
    """Testa extração simples de página"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as output:
        output_path = output.name

    try:
        result = subprocess.run(
            ["bun", "run", "web2md.ts", "https://example.com", "--out", output_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert os.path.exists(output_path), "Arquivo não criado"
        with open(output_path) as f:
            content = f.read()
            assert len(content) > 0, "Arquivo vazio"
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)
```

## ⚡ Performance Tests

### Locust Configuration

```python
class Web2MDUser(HttpUser):
    """Simula usuário usando web2md"""
    wait_time = between(1, 3)

    @task
    def extract_simple_page(self):
        """Testa extração de página simples"""
        self.client.get("/")

    @task(3)
    def extract_article(self):
        """Testa extração de artigo (3x mais frequente)"""
        self.client.get("/article")
```

### Métricas

- **Simple pages:** <5s
- **JavaScript pages:** <10s
- **Throughput:** >1 request/s
- **Token economy:** >85%

## 📈 Coverage

### Meta

- **Cobertura mínima:** 80%
- **Cobertura alvo:** 90%

### Relatórios

```bash
# Gerar coverage report
pytest tests/unit/ --cov=. --cov-report=html

# Abrir no browser
open htmlcov/index.html
```

## 🔍 Code Quality

### Flake8 (Style)

```bash
flake8 . --exclude=node_modules,dist,build
```

### Mypy (Type Checking)

```bash
mypy . --ignore-missing-imports
```

### Bandit (Security)

```bash
bandit -r . -f json -o bandit-report.json
```

## 🔄 CI/CD Integration

### GitLab CI Stages

```yaml
stages:
  - test
  - performance
  - quality

test-bdd:
  stage: test
  script:
    - behave tests/features/

test-unit:
  stage: test
  script:
    - pytest tests/unit/

performance:
  stage: performance
  script:
    - locust -f locustfile.py --headless --users 10 --run-time 30s

quality:
  stage: quality
  script:
    - flake8 . --exclude=node_modules
    - bandit -r . -f json -o bandit-report.json
```

## 📝 Escrevendo Novos Testes

### BDD Steps

1. Adicionar cenário em `tests/features/web2md-full.feature`
2. Implementar step em `tests/steps/web2md_steps.py`
3. Rodar: `behave tests/features/`

### TDD Tests

1. Adicionar teste em `tests/unit/test_web2md.py`
2. Rodar: `pytest tests/unit/ -v`

### Performance Tests

1. Adicionar task em `locustfile.py`
2. Rodar: `locust -f locustfile.py --headless`

## 🎓 Convenções

### Nomenclatura

- **Features:** `nome-da-feature.feature`
- **Steps:** `nome_steps.py`
- **Unit tests:** `test_<module>.py`
- **Test classes:** `Test<Feature>`

### Estrutura

```python
def test_<feature>_<scenario>(self):
    """Testa <feature> em <scenario>"""
    # Given
    setup()

    # When
    result = action()

    # Then
    assert result == expected
```

## 🐛 Debugging

### Behave Debug

```bash
behave tests/features/ --debug
```

### Pytest Debug

```bash
pytest tests/unit/ -v --pdb
```

### Logs

Logs são salvos em:

- `reports/behave-report.txt`
- `htmlcov/index.html`
- `bandit-report.json`

---

**Baseado em:** Pesquisa experimental com web2md + auto-research
**Metodologia:** TDD + BDD com critérios de aceitação
**Próxima atualização:** Quando novos requisitos surgirem
