# Auto Prompt Generation System

Sistema inteligente de geração de prompts para subagentic programming, integrando web2md + Advanced RAG + Code Graph.

## Visão Geral

O Auto Prompt Generation System analisa tarefas, coleta contexto relevante de múltiplas fontes (RAG semântico, grafo de código, documentação externa) e gera prompts otimizados automaticamente para subagentes.

### Arquitetura

```
Task Description
    ↓
Task Classifier (type, complexity, expertise)
    ↓
Context Aggregation (RAG + Code Graph + web2md)
    ↓
Prompt Generator (template-based with context injection)
    ↓
Quality Validator (score > 0.8)
    ↓
Optimized Prompt
```

## Instalação

```bash
cd /Users/lucascardoso/web2md/auto-prompt
```

## Uso

### CLI

#### Gerar Prompt

```bash
python cli.py generate "Implement user authentication with JWT"
```

Com opções:

```bash
python cli.py generate "Implement user authentication" \
  --complexity medium \
  --output /tmp/auth_prompt.md
```

#### Analisar Task

```bash
python cli.py analyze "Add pagination to web2md results"
```

Saída:
```
📋 Task Type: implementation
📊 Complexity: medium
🎯 Expertise: backend
📈 Confidence: 0.85
🚀 Suggested Strategy: parallel
🤖 Suggested Model: sonnet
📏 Estimated Tokens: 2000
```

#### Validar Prompt

```bash
python cli.py validate /tmp/auth_prompt.md --threshold 0.8
```

### Python API

```python
import asyncio
from auto_prompt.core import AutoPromptGenerator

async def main():
    generator = AutoPromptGenerator()

    result = await generator.generate_prompt(
        "Implement user authentication with JWT",
        constraints={"complexity": "medium"}
    )

    print(result.prompt)
    print(f"Quality Score: {result.quality_score}")
    print(f"Model: {result.metadata['model']}")

asyncio.run(main())
```

## Componentes

### 1. Task Classifier

Analisa a descrição da task e determina:
- **Tipo**: implementation, refactoring, debugging, research
- **Complexidade**: low, medium, high
- **Expertise**: frontend, backend, fullstack, devops, data, security
- **Estratégia**: parallel, sequential, hybrid
- **Modelo**: sonnet, haiku, opus

### 2. Context Aggregator

Coleta contexto de múltiplas fontes:
- **Advanced RAG MCP**: Busca semântica no codebase
- **Code Graph MCP**: Análise de dependências e impacto
- **web2md**: Documentação externa

### 3. Prompt Generator

Gera prompts otimizados usando:
- Templates estruturados por tipo de task
- Injeção dinâmica de contexto
- Otimização de tokens
- Validação de qualidade

### 4. Quality Validator

Valida prompts com base em:
- Descrição clara da task
- Presença de contexto/instruções
- Existência de deliverables
- Comprimento apropriado
- Estrutura bem definida

## Templates

Templates disponíveis em `templates/prompts.json`:

- **implementation**: Para novas funcionalidades
- **refactoring**: Para refatoração de código
- **debugging**: Para debugging de issues
- **research**: Para pesquisa e investigação

### Criar Novo Template

```python
from auto_prompt.core import TemplateEngine

engine = TemplateEngine()
engine.add_template(
    name="testing",
    template="# Test: {feature}\n\n...",
    context_sources=["semantic_search"],
    required_variables=["feature"],
    metadata={"complexity": "low"}
)
```

## Integração com autonomous-automation

Adicionar à skill autonomous-automation:

```markdown
## Phase 1.5: Auto Prompt Generation

### Generate Prompt
```bash
auto-prompt generate --task "Implement feature X" --output /tmp/prompt.md
```

### Validate Quality
```bash
auto-prompt validate /tmp/prompt.md --threshold 0.8
```

### Use in Tracks
```bash
research_prompt=$(auto-prompt generate --task "Research similar features")
spawn_subagent "$research_prompt" → track_result
```
```

## Métricas de Qualidade

### Prompt Quality Score

- **0.8 - 1.0**: Excelente, pronto para usar
- **0.6 - 0.8**: Bom, pode precisar de ajustes
- **0.4 - 0.6**: Aceitável, requer revisão
- **0.0 - 0.4**: Insuficiente, precisa ser regenerado

### Fatores que Influenciam o Score

1. Descrição clara da task (25%)
2. Presença de contexto/instruções (25%)
3. Existência de deliverables (25%)
4. Comprimento apropriado (25%)
5. Estrutura bem definida (bônus 10%)

## Exemplos

### Exemplo 1: Implementação

```bash
python cli.py generate "Implement pagination for web2md results"
```

### Exemplo 2: Debugging

```bash
python cli.py generate "Fix memory leak in web2md TypeScript code"
```

### Exemplo 3: Refatoração

```bash
python cli.py generate "Refactor web2md.ts to use async/await patterns"
```

### Exemplo 4: Pesquisa

```bash
python cli.py generate "Research best practices for HTML to Markdown conversion"
```

## Desenvolvimento

### Executar Testes

```bash
# Unit tests
pytest auto-prompt/tests/test_classifier.py -v

# Integration tests
pytest auto-prompt/tests/test_generator.py -v

# All tests
pytest auto-prompt/tests/ -v
```

### Adicionar Novo Tipo de Task

1. Adicionar keywords ao `TaskClassifier`
2. Criar template em `templates/prompts.json`
3. Adicionar testes em `tests/`

## Troubleshooting

### MCP Servers Não Carregam

```bash
# Verificar se MCP servers estão rodando
claude mcp list | grep -E "(code-graph|advanced-rag)"

# Deve mostrar:
# code-graph: ✓ Connected
# advanced-rag: ✓ Connected
```

### Prompt Quality Score Baixo

- Verificar se o template tem todos os campos obrigatórios
- Adicionar mais contexto relevante
- Melhorar a descrição da task
- Revisar estrutura do prompt

## Roadmap

- [ ] Subagent Orchestrator (spawn múltiplos subagentes)
- [ ] Result Aggregator (consolidar resultados)
- [ ] Feedback Loop (aprender com resultados)
- [ ] A/B Testing de prompts
- [ ] Métricas de efetividade

## Contribuindo

1. Fork o projeto
2. Crie branch para feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push para branch (`git push origin feature/AmazingFeature`)
5. Abra Pull Request

## Licença

MIT License - ver arquivo LICENSE para detalhes
