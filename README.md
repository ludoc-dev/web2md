# web2md - Web to Markdown Converter

Extraia conteúdo limpo e estruturado de qualquer página web. Perfeito para alimentar LLMs com contexto otimizado (90% economia de tokens).

## 🚀 Quick Start

```bash
cd ~/web2md
bun install

# Extração básica
bun run web2md.ts https://example.com/article

# Salvar em arquivo
bun run web2md.ts https://example.com --out article.md

# Com JavaScript rendering (SPAs)
bun run web2md.ts --js https://spa-example.com --out spa.md
```

## 📋 Usage Patterns

### Pattern 1: Direct Extraction

```bash
bun run web2md.ts <URL> > output.md
```

### Pattern 2: Save to File

```bash
bun run web2md.ts <URL> --out path/to/file.md
```

### Pattern 3: JavaScript Rendering

```bash
bun run web2md.ts --js <URL>
```

### Pattern 4: Piping

```bash
bun run web2md.ts <URL> | other-tool
```

## 🔧 How It Works

### Pipeline

1. **Fetch HTML** - Download raw HTML da URL
2. **Virtual DOM** - Parse com JSDOM
3. **Clean Content** - Remove ruído com Readability
4. **Convert to Markdown** - Transforma com TurndownService

### Flags

- `--js` - Usa Playwright para JavaScript rendering
- `--out <file>` - Salva em arquivo ao invés de stdout

### Output

- **Default:** stdout (printa no terminal)
- **File:** Salva no path especificado
- **Format:** Markdown puro com headers, lists, links, code blocks

## 🎯 Best Use Cases

### For LLM Context

- Extração de artigos
- Limpeza de documentação
- Preparação de research papers
- Sumarização de web content

### For Development

- Migração de conteúdo
- Geração de documentação
- Criação de arquivos
- Extração de texto

## 📦 Dependencies

- **Runtime:** Bun
- **Core:** jsdom, @mozilla/readability, turndown
- **Optional:** playwright (para flag --js)

## 🧪 Testing (BDD/TDD)

Este projeto segue metodologia TDD com critérios de aceitação baseados em pesquisa.

### Estrutura de Testes

```
tests/
├── features/           # BDD scenarios (Behave)
│   └── web2md-extraction.feature
├── acceptance/         # Acceptance criteria
│   └── test-criteria.md
└── unit/              # TDD unit tests (Pytest)
    └── test_web2md.py
```

### Critérios de Aceitação

Baseados em pesquisa experimental:

- ✅ **90% economia de tokens** (15K → 1.5K tokens)
- ✅ **<5s para páginas simples**
- ✅ **Remoção de ruído** (ads, navbars, sidebars)
- ✅ **Preservação de estrutura** (headers, lists, code blocks)

### Rodar Testes

```bash
# Unit tests
pytest tests/unit/ -v

# BDD scenarios
behave tests/features/

# Performance tests
locust -f locustfile.py --headless
```

## 🐳 Docker Deployment

### Build

```bash
docker-compose build
```

### Run

```bash
docker-compose up -d
```

### Services

- **web2md** - Serviço principal
- **test-runner** - Testes automatizados
- **gitlab-runner** - CI/CD integration
- **locust-ui** - Performance testing

## 🔄 CI/CD Pipeline

### GitLab CI Stages

1. **discover** - Auto-research de novas ferramentas
2. **setup** - Setup do ambiente
3. **test** - Unit + BDD tests
4. **performance** - Locust load tests
5. **quality** - Flake8, mypy, bandit
6. **report** - Relatório final

### Quality Gates

- **Cobertura:** >80%
- **Performance:** <5s página simples
- **Token economy:** >85%
- **Security:** Sem vulnerabilidades críticas

## 📚 Research & Discovery

Este projeto é parte de um sistema maior de pesquisa e descoberta de ferramentas.

### Auto-Research System

```bash
# Executar pesquisa automatizada
~/.claude/research/auto-research.sh
```

### Research Registry

- [AI CLI Tools](~/.claude/research/README.md#-ai-cli-tools) - 15+ ferramentas avaliadas
- [Rust Tools](~/.claude/research/README.md#-rust-tools) - Ferramentas descobertas
- [CI/CD Methodologies](~/.claude/research/README.md#-cicd-methodologies) - Abordagens documentadas

### Padrões de Pesquisa

**Fontes que funcionam:**

- ✅ GitHub Topics
- ✅ Hacker News
- ✅ Documentação oficial (com web2md)

**Fontes que NÃO funcionam:**

- ❌ DuckDuckGo (bot detection)
- ❌ Reddit (timeout)
- ❌ StackOverflow (muito pesado)

## 🎯 Acceptance Criteria

### Critério 1: Economia de Tokens

**Aceitação:** 90% redução vs HTML

```gherkin
Dado que página HTML tem 15.000 tokens
Quando executo web2md
Então Markdown resultante tem <1.500 tokens
E economia é >85%
```

### Critério 2: Performance

**Aceitação:** Tempo de processamento

```gherkin
Dado que acesso página simples
Quando executo web2md
Então processa em <5 segundos
E latência é aceitável
```

### Critério 3: Qualidade de Extração

**Aceitação:** Conteúdo principal preservado

```gherkin
Dado que acesso artigo com formatação
Quando executo web2md
Então Markdown contém artigo completo
E ruído foi removido
```

### Critério 4: Remoção de Ruído

**Aceitação:** Sem elementos de ruído

```gherkin
Dado que página tem ads, navbar, sidebar
Quando executo web2md
Então Markdown não contém ruído
E apenas conteúdo principal
```

### Critério 5: Preservação de Estrutura

**Aceitação:** Estrutura HTML preservada

```gherkin
Dado que página tem headers, lists, code blocks
Quando executo web2md
Então Markdown tem estrutura equivalente
E formatação é válida
```

## 📊 Performance

- **Simple pages:** ~0.1-0.5 segundos
- **JavaScript pages:** ~2-5 segundos (com --js)
- **Token efficiency:** 90%+ redução vs HTML original

## 🔍 Error Handling

- Network errors → stderr
- Invalid URLs → stderr + exit
- Parse errors → stderr + exit
- Success → stdout (Markdown only)

## 💡 Tips

1. **Start sem --js** - Mais rápido, funciona para a maioria dos sites
2. **Use --js para SPAs** - React, Vue, Angular apps
3. **Pipe para arquivos** - Fácil salvar output
4. **Combine com outras tools** - Build pipelines

## 🛠️ Technical Details

### Fetch Strategy

- **Default:** Simple HTTP fetch (fastest)
- **With --js:** Playwright headless browser (handles SPAs)

### Content Cleaning

- Mozilla Readability algorithm
- Remove: ads, navbars, sidebars, footers
- Preserve: main content, headings, lists, links, code blocks

### Markdown Conversion

- Preserva headers (h1-h6)
- Mantém estrutura de listas
- Converte links para formato Markdown
- Formata code blocks com language tags

---

**Desenvolvido com:** TDD + BDD + Docker + GitLab CI
**Research:** Auto-research system + web2md
**Docs baseadas em:** Acceptance criteria de pesquisa experimental
