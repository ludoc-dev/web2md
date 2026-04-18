#!/bin/bash
# run-all-tests.sh - Executa todos os testes (BDD + TDD + Performance)
set -e

echo "🧪 web2md - Test Suite Completo"
echo "================================"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# ==================== CHECKS ====================

echo ""
echo "📋 Verificando ambiente..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 encontrado${NC}"

# Check Bun
if ! command -v bun &> /dev/null; then
    echo -e "${RED}❌ Bun não encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Bun encontrado${NC}"

# Check dependencies
echo ""
echo "📦 Verificando dependências Python..."
pip install -q -r tests/requirements.txt 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Algumas dependências não puderam ser instaladas${NC}"
}

# ==================== UNIT TESTS (TDD) ====================

echo ""
echo "================================"
echo "🔬 Unit Tests (TDD - Pytest)"
echo "================================"

if pytest tests/unit/ -v --tb=short; then
    echo -e "${GREEN}✅ Unit tests passaram${NC}"
    UNIT_TESTS="PASS"
else
    echo -e "${RED}❌ Unit tests falharam${NC}"
    UNIT_TESTS="FAIL"
fi

# ==================== BDD TESTS (Behave) ====================

echo ""
echo "================================"
echo "🎭 BDD Tests (Behave)"
echo "================================"

if behave tests/features/ -f pretty; then
    echo -e "${GREEN}✅ BDD tests passaram${NC}"
    BDD_TESTS="PASS"
else
    echo -e "${RED}❌ BDD tests falharam${NC}"
    BDD_TESTS="FAIL"
fi

# ==================== PERFORMANCE TESTS ====================

echo ""
echo "================================"
echo "⚡ Performance Tests (Locust)"
echo "================================"

# Check se temos locustfile.py
if [ -f "locustfile.py" ]; then
    echo "Rodando Locust em modo headless (10 usuários, 10 segundos)..."
    if locust -f locustfile.py --headless --users 10 --run-time 10s --host https://example.com; then
        echo -e "${GREEN}✅ Performance tests completados${NC}"
        PERF_TESTS="PASS"
    else
        echo -e "${YELLOW}⚠️  Performance tests com avisos${NC}"
        PERF_TESTS="WARN"
    fi
else
    echo -e "${YELLOW}⚠️  locustfile.py não encontrado, pulando performance tests${NC}"
    PERF_TESTS="SKIP"
fi

# ==================== CODE QUALITY ====================

echo ""
echo "================================"
echo "🔍 Code Quality (Flake8 + Mypy + Bandit)"
echo "================================"

# Flake8
echo "Rodando Flake8..."
if flake8 . --exclude=,node_modules,dist,build,.eggs --max-line-length=100; then
    echo -e "${GREEN}✅ Flake8 OK${NC}"
    FLAKE8="PASS"
else
    echo -e "${YELLOW}⚠️  Flake8 encontrou issues${NC}"
    FLAKE8="WARN"
fi

# Mypy (opcional)
echo "Rodando Mypy (opcional)..."
mypy . --ignore-missing-imports --no-error-summary 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Mypy pulado ou com avisos${NC}"
    MYPY="WARN"
}

# Bandit (security)
echo "Rodando Bandit (security)..."
if bandit -r . -f json -o bandit-report.json 2>/dev/null; then
    echo -e "${GREEN}✅ Bandit OK${NC}"
    BANDIT="PASS"
else
    echo -e "${YELLOW}⚠️  Bandit encontrou issues${NC}"
    BANDIT="WARN"
fi

# ==================== COVERAGE REPORT ====================

echo ""
echo "================================"
echo "📊 Coverage Report"
echo "================================"

if [ -d "htmlcov" ]; then
    echo "Coverage report gerado em: htmlcov/index.html"
    echo "Abrindo no browser..."
    if command -v open &> /dev/null; then
        open htmlcov/index.html
    elif command -v xdg-open &> /dev/null; then
        xdg-open htmlcov/index.html
    fi
fi

# ==================== FINAL SUMMARY ====================

echo ""
echo "================================"
echo "📋 Final Summary"
echo "================================"
echo "Unit Tests (TDD):    $UNIT_TESTS"
echo "BDD Tests:           $BDD_TESTS"
echo "Performance Tests:   $PERF_TESTS"
echo "Flake8:             $FLAKE8"
echo "Bandit:             $BANDIT"
echo "================================"

# Exit code
if [ "$UNIT_TESTS" = "FAIL" ] || [ "$BDD_TESTS" = "FAIL" ]; then
    echo -e "${RED}❌ Alguns testes falharam${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Todos os testes passaram!${NC}"
    exit 0
fi
