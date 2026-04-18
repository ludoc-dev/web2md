#!/bin/bash
# run-docker-tests.sh - Executa todos os testes em containers (Docker ou Podman)
set -e

# Auto-detectar container engine
CONTAINER_CMD=""
if command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
    COMPOSE_CMD="podman-compose"
elif command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Nem Docker nem Podman encontrado"
    exit 1
fi

echo "🐳 Usando: $CONTAINER_CMD"
echo "📦 Compose: $COMPOSE_CMD"

echo "🐳 web2md - Docker Test Suite"
echo "=============================="

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ==================== BUILD ====================

echo ""
echo "🔨 Building images com $CONTAINER_CMD..."
$COMPOSE_CMD -f docker-compose.test.yml build

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build falhou${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Build completo${NC}"

# ==================== START CONTAINERS ====================

echo ""
echo "🚀 Starting containers com $CONTAINER_CMD..."
$COMPOSE_CMD -f docker-compose.test.yml up -d

# Esperar containers estarem prontos
echo "⏳ Waiting for containers..."
sleep 5

# ==================== UNIT TESTS (TDD) ====================

echo ""
echo "=============================="
echo "🔬 Unit Tests (TDD - Pytest)"
echo "=============================="

docker exec test-runner pytest tests/unit/ -v --tb=short

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Unit tests passaram${NC}"
    UNIT_TESTS="PASS"
else
    echo -e "${RED}❌ Unit tests falharam${NC}"
    UNIT_TESTS="FAIL"
fi

# ==================== BDD TESTS ====================

echo ""
echo "=============================="
echo "🎭 BDD Tests (Behave)"
echo "=============================="

docker exec test-runner behave tests/features/ -f pretty

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ BDD tests passaram${NC}"
    BDD_TESTS="PASS"
else
    echo -e "${RED}❌ BDD tests falharam${NC}"
    BDD_TESTS="FAIL"
fi

# ==================== PERFORMANCE TESTS ====================

echo ""
echo "=============================="
echo "⚡ Performance Tests (Locust)"
echo "=============================="

echo "Iniciando Locust em modo headless..."
docker exec locust locust --locustfile /mnt/locustfile.py --headless --users 10 --run-time 10s --host https://example.com

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Performance tests completados${NC}"
    PERF_TESTS="PASS"
else
    echo -e "${YELLOW}⚠️  Performance tests com avisos${NC}"
    PERF_TESTS="WARN"
fi

# ==================== CODE QUALITY ====================

echo ""
echo "=============================="
echo "🔍 Code Quality"
echo "=============================="

# Flake8
echo "Rodando Flake8..."
docker exec test-runner flake8 . --exclude=node_modules,dist,build,.eggs --max-line-length=100

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Flake8 OK${NC}"
    FLAKE8="PASS"
else
    echo -e "${YELLOW}⚠️  Flake8 encontrou issues${NC}"
    FLAKE8="WARN"
fi

# Bandit
echo "Rodando Bandit (security)..."
docker exec test-runner bandit -r . -f json -o reports/bandit-report.json 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Bandit OK${NC}"
    BANDIT="PASS"
else
    echo -e "${YELLOW}⚠️  Bandit encontrou issues${NC}"
    BANDIT="WARN"
fi

# ==================== COVERAGE REPORT ====================

echo ""
echo "=============================="
echo "📊 Coverage Report"
echo "=============================="

docker exec test-runner pytest tests/unit/ --cov=. --cov-report=html --cov-report=term

echo "Coverage report gerado em: htmlcov/index.html"

# ==================== FINAL SUMMARY ====================

echo ""
echo "=============================="
echo "📋 Final Summary"
echo "=============================="
echo "Unit Tests (TDD):    $UNIT_TESTS"
echo "BDD Tests:           $BDD_TESTS"
echo "Performance Tests:   $PERF_TESTS"
echo "Flake8:             $FLAKE8"
echo "Bandit:             $BANDIT"
echo "=============================="

# ==================== CLEANUP ====================

echo ""
echo "🧹 Cleaning up com $CONTAINER_CMD..."
$COMPOSE_CMD -f docker-compose.test.yml down

# Exit code
if [ "$UNIT_TESTS" = "FAIL" ] || [ "$BDD_TESTS" = "FAIL" ]; then
    echo -e "${RED}❌ Alguns testes falharam${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Todos os testes passaram!${NC}"
    exit 0
fi
