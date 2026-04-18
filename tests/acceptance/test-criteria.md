# Critérios de Aceitação - Testes BDD (TDD)

## 🎯 Filosofia de Testes

**TDD (Test-Driven Development):**
1. **Escrever teste primeiro** (Red, Green, Refactor)
2. **Critérios de aceitação claros**
3. **Spec baseada no que foi pesquisado**

**BDD (Behavior-Driven Development):**
1. **Cenários de teste** em linguagem natural
2. **Critérios de aceitação explícitos**
3. **Foco no comportamento** do sistema

## 📋 Estrutura de Testes

### **1. Acceptance Tests (Behave)**
- **Localização:** `tests/features/`
- **Foco:** Comportamento do usuário
- **Critérios:** Aceitação do produto
- **Based on:** Descobertas de pesquisa

### **2. Unit Tests (Pytest)**
- **Localização:** `tests/unit/`
- **Foco:** Funções individuais
- **Critérios:** Cobertura >80%
- **Based on:** Implementação

### **3. Performance Tests (Locust)**
- **Localização:** `locustfile.py`
- **Foco:** Carga e latência
- **Critérios:** <5s página simples
- **Based on:** Métricas reais

## 🎯 Critérios de Aceitação (Baseado em Pesquisa)

### **web2md - Extração de Conteúdo**

#### **Critério 1: Economia de Tokens**
**Aceitação:** 90% redução vs HTML
```gherkin
Dado que página HTML tem 15.000 tokens
Quando executo web2md
Então Markdown resultante tem <1.500 tokens
E economia é >85%
```

#### **Critério 2: Performance**
**Aceitação:** Tempo de processamento
```gherkin
Dado que acesso página simples
Quando executo web2md
Então processa em <5 segundos
E latência é aceitável
```

#### **Critério 3: Qualidade de Extração**
**Aceitação:** Conteúdo principal preservado
```gherkin
Dado que acesso artigo com formatação
Quando executo web2md
Então Markdown contém artigo completo
E ruído foi removido
```

#### **Critério 4: Remoção de Ruído**
**Aceitação:** Sem elementos de ruído
```gherkin
Dado que página tem ads, navbar, sidebar
Quando executo web2md
Então Markdown não contém ruído
E apenas conteúdo principal
```

#### **Critério 5: Preservação de Estrutura**
**Aceitação:** Estrutura HTML preservada
```gherkin
Dado que página tem headers, lists, code blocks
Quando executo web2md
Então Markdown tem estrutura equivalente
E formatação é válida
```

### **Sistema Autônomo - Discovery**

#### **Critério 1: Descoberta de Ambiente**
**Aceitação:** Identificação correta de recursos
```gherkin
Dado que executo discover-environment.sh
Quando sistema analisa ambiente local
Então detecta CPU, RAM, portas, tools
E informações são salvas em cache
```

#### **Critério 2: Auto-Research**
**Aceitação:** Pesquisa automatizada funciona
```gherkin
Dado que executo auto-research.sh
Quando sistema pesquisa novas ferramentas
Então extrai docs com web2md
E salva em discovered/ organizado
```

#### **Critério 3: Registro Sistemático**
**Aceitação:** Descobertas são registradas
```gherkin
Dado que faço uma descoberta
Quando salvo em research/discovered/
Então sigo padrão de patterns.md
E agents.md pode ser atualizado
```

### **CI/CD - Pipeline**

#### **Critério 1: Pipeline Completo**
**Aceitação:** 6 stages executam em ordem
```gherkin
Dado que push código
Quando pipeline GitLab CI dispara
Então stages executam: discover → setup → test → performance → quality → report
E relatório final é gerado
```

#### **Critério 2: Quality Gates**
**Aceitação:** Testes de qualidade passam
```gherkin
Dado que pipeline executa stage quality
Quando roda flake8, mypy, bandit
Então código segue padrões
E segurança é verificada
```

#### **Critério 3: Auto-Research Integrado**
**Aceitação:** Descoberta automatizada no pipeline
```gherkin
Dado que pipeline executa stage discover
Quando auto-research.sh roda
Então novas descobertas são feitas
E artifacts são salvos
```

## 📊 Matriz de Rastreabilidade

| Critério | Fonte | Status | Teste Implementado |
|----------|-------|--------|-------------------|
| 90% economia tokens | web2md docs | ✅ Confirmado | Behave |
| <5s página simples | web2md docs | ✅ Confirmado | Behave |
| Remoção ruído | web2md docs | ✅ Confirmado | Behave |
| Estrutura preservada | web2md docs | ✅ Confirmado | Behave |
| Discovery cache | agents.md | ✅ Confirmado | - |
| Auto-research | patterns.md | ✅ Confirmado | - |
| Pipeline stages | GitLab docs | ✅ Confirmado | .gitlab-ci.yml |
| Quality gates | Best practices | ✅ Confirmado | flake8, mypy, bandit |

## 🔄 Workflow TDD

### **1. Red (Escrever teste falho)**
```gherkin
Feature: Nova funcionalidade
  Scenario: Teste básico falha
    When executo X
    Then deveria acontecer Y (mas ainda não implementado)
```

### **2. Green (Fazer teste passar)**
```python
# Implementação mínima para teste passar
def nova_funcionalidade():
    return "Y"  # Implementação simples
```

### **3. Refactor (Melhorar código)**
```python
# Refatorar com qualidade
def nova_funcionalidade_otimizada():
    # Implementação melhorada
    return "Y" com melhor performance
```

## 🎯 Prioridades de Teste

### **Alta Prioridade (P1)**
1. web2md extração básica
2. Remoção de ruído
3. Performance (<5s)

### **Média Prioridade (P2)**
4. Preservação de estrutura
5. Sistema autônomo discovery
6. Auto-research

### **Baixa Prioridade (P3)**
7. Quality gates (flake8, mypy)
8. Performance avançada
9. Security scanning

---

**Lembre:** TDD = Escrever teste PRIMEIRO, implementar depois.
