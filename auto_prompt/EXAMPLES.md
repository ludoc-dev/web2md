# Auto Prompt Examples

Exemplos práticos de uso do Auto Prompt Generation System.

## Exemplo 1: Implementação Simples

```bash
python cli.py generate "Implement user authentication with JWT"
```

**Saída Esperada:**
```
📊 Quality Score: 0.85
🔧 Model: sonnet
📏 Estimated Tokens: 2500
📋 Task Type: implementation
📊 Complexity: medium
🎯 Strategy: parallel
📚 Context Sources: semantic_search
```

## Exemplo 2: Task Complexa com High Complexity

```bash
python cli.py generate "Build comprehensive distributed authentication system" \
  --complexity high \
  --output /tmp/auth_system_prompt.md
```

## Exemplo 3: Análise de Task

```bash
python cli.py analyze "Add pagination to web2md results"
```

**Saída:**
```
📋 Task Type: implementation
📊 Complexity: medium
🎯 Expertise: backend
📈 Confidence: 0.85
🚀 Suggested Strategy: parallel
🤖 Suggested Model: sonnet
📏 Estimated Tokens: 2000
```

## Exemplo 4: Validação de Prompt

```bash
python cli.py validate /tmp/auth_prompt.md --threshold 0.8
```

**Se válido:**
```
✅ Valid - Quality Score: 0.85
```

**Se inválido:**
```
❌ Invalid - Quality Score: 0.65 (threshold: 0.80)

⚠️  Issues:
  - Missing deliverables or requirements

💡 Suggestions:
  - Add deliverables or requirements section (e.g., '## Deliverables')
```

## Exemplo 5: Python API

```python
import asyncio
from auto_prompt.core import AutoPromptGenerator

async def main():
    generator = AutoPromptGenerator()

    # Generate prompt
    result = await generator.generate_prompt(
        "Implement user authentication with JWT",
        constraints={"complexity": "medium"}
    )

    # Use the prompt
    print(result.prompt)
    print(f"Quality: {result.quality_score}")

    # Save to file
    with open("/tmp/auth_prompt.md", "w") as f:
        f.write(result.prompt)

asyncio.run(main())
```

## Exemplos de Tasks por Categoria

### Implementação

```bash
# Backend
python cli.py generate "Implement REST API for user management"

# Frontend
python cli.py generate "Create React component for user profile"

# Fullstack
python cli.py generate "Build fullstack authentication system"
```

### Refatoração

```bash
# Module refactoring
python cli.py generate "Refactor authentication module for better maintainability"

# Performance optimization
python cli.py generate "Optimize database queries in user service"

# Code cleanup
python cli.py generate "Clean up deprecated code in web2md"
```

### Debugging

```bash
# Bug fix
python cli.py generate "Fix memory leak in authentication service"

# Error handling
python cli.py generate "Handle timeout errors in API calls"

# Integration issue
python cli.py generate "Fix CORS issues between frontend and backend"
```

### Pesquisa

```bash
# Best practices
python cli.py generate "Research JWT authentication best practices"

# Technology comparison
python cli.py generate "Compare TypeScript vs JavaScript for web development"

# Architecture patterns
python cli.py generate "Research microservices patterns for authentication"
```

## Integração com autonomous-automation

### No arquivo SKILL.md:

```markdown
## Phase 1.5: Auto Prompt Generation

### Generate Prompt for Track

```bash
# Research track
research_prompt=$(auto-prompt generate --task "Research similar authentication patterns")
spawn_subagent "$research_prompt" → track_1_result

# Implementation track
implementation_prompt=$(auto-prompt generate --task "Implement authentication core logic")
spawn_subagent "$implementation_prompt" → track_2_result

# Testing track
testing_prompt=$(auto-prompt generate --task "Create comprehensive tests for authentication")
spawn_subagent "$testing_prompt" → track_3_result
```

### Validate Quality

```bash
# Before using prompt
auto-prompt validate /tmp/generated_prompt.md --threshold 0.8

# Only use if valid
if [ $? -eq 0 ]; then
  spawn_subagent "$(cat /tmp/generated_prompt.md)"
fi
```
```

## Casos de Uso Avançados

### Caso 1: Task com Múltiplas Subtasks

```bash
# Decompose complex task
main_task="Build authentication system"

# Generate prompts for subtasks
python cli.py generate "Design authentication database schema" \
  --output /tmp/subtask_1_prompt.md

python cli.py generate "Implement authentication API" \
  --output /tmp/subtask_2_prompt.md

python cli.py generate "Create authentication tests" \
  --output /tmp/subtask_3_prompt.md
```

### Caso 2: Iteração em Prompt

```bash
# Generate initial prompt
python cli.py generate "Implement authentication" \
  --output /tmp/prompt_v1.md

# Validate
python cli.py validate /tmp/prompt_v1.md

# If score is low, add more context and regenerate
python cli.py generate "Implement JWT-based authentication with refresh tokens" \
  --complexity high \
  --output /tmp/prompt_v2.md

# Compare quality scores
python cli.py validate /tmp/prompt_v1.md
python cli.py validate /tmp/prompt_v2.md
```

### Caso 3: Batch Generation

```bash
# Generate prompts for multiple related tasks
tasks=(
  "Design database schema"
  "Implement API endpoints"
  "Create frontend components"
  "Write unit tests"
  "Add documentation"
)

for task in "${tasks[@]}"; do
  filename=$(echo "$task" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
  python cli.py generate "$task" --output "/tmp/${filename}_prompt.md"
done
```

## Dicas e Melhores Práticas

### 1. Seja Específico

❌ Ruim:
```bash
python cli.py generate "Implement authentication"
```

✅ Bom:
```bash
python cli.py generate "Implement JWT-based authentication with access tokens and refresh tokens"
```

### 2. Use Complexidade Apropriada

❌ Ruim:
```bash
python cli.py generate "Fix simple bug" --complexity high
```

✅ Bom:
```bash
python cli.py generate "Fix simple bug" --complexity low
```

### 3. Valide Sempre

```bash
# Sempre validar antes de usar
python cli.py generate "Implement feature" --output /tmp/prompt.md
python cli.py validate /tmp/prompt.md --threshold 0.8
```

### 4. Revise e Ajuste

```bash
# Gerar prompt
python cli.py generate "Implement authentication" --output /tmp/prompt.md

# Revisar manualmente
cat /tmp/prompt.md

# Adicionar contexto específico se necessário
vim /tmp/prompt.md
```

## Troubleshooting

### Problema: Quality Score Baixo

**Causa:** Prompt muito genérico ou sem contexto suficiente

**Solução:**
- Adicionar mais detalhes à task
- Especificar tecnologia/framework
- Incluir requisitos específicos

### Problema: Task Type Incorreto

**Causa:** Descrição ambígua da task

**Solução:**
- Usar verbos específicos (implement, refactor, debug, research)
- Incluir contexto técnico
- Verificar com `analyze` primeiro

### Problema: Prompt Muito Longo

**Causa:** Task muito complexa ou contexto excessivo

**Solução:**
- Dividir em subtasks menores
- Usar `--complexity low` para prompts mais focados
- Remover contexto não essencial

## Conclusão

Estes exemplos demonstram como usar o Auto Prompt Generation System para gerar prompts otimizados automaticamente. O sistema integra contexto de múltiplas fontes (RAG, Code Graph, web2md) para criar prompts de alta qualidade para subagentes.
