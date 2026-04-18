#!/usr/bin/env python3
"""
locustfile.py - Configuração de teste de carga para web2md
Testa performance de extração de conteúdo web
"""

from locust import HttpUser, task, between, events

class Web2MDUser(HttpUser):
    """Simula usuário usando web2md"""

    def on_start(self):
        """Ao iniciar"""
        self.host = "https://example.com"

    @task
    def extract_simple_page(self):
        """Testa extração de página simples"""
        self.client.get("/")

    @task(3)
    def extract_article(self):
        """Testa extração de artigo (3x mais frequente)"""
        self.client.get("/article")

    @task
    def extract_docs(self):
        """Testa extração de documentação"""
        self.client.get("/docs")

    @task(2)
    def extract_with_js(self):
        """Testa extração com JavaScript (2x mais pesado)"""
        self.client.get("/spa")


class Web2MDUserWithAuth(HttpUser):
    """Simula usuário autenticado"""

    def on_start(self):
        self.client.post("/login", json={
            "username": "test_user",
            "password": "test_pass"
        })

    @task
    def extract_protected(self):
        """Testa extração de conteúdo protegido"""
        self.client.get("/protected")


# ========================================
# CONFIGURAÇÕES
# ========================================

# Wait time entre requests (simula usuário real)
wait_time = between(1, 3)

# Peso das tarefas (distribuição)
weight = 1

# Taxa de_spawn (usuários por segundo)
# Ajustar conforme capacidade do servidor
spawn_rate = 1

# Host alvo (para testes locais)
host = "https://example.com"


# ========================================
# EVENTS HANDLERS
# ========================================

@events.request.add_listener
def on_request(request_context, response):
    """Log de cada request"""
    if response.exception:
        print(f"Request failed: {request_context.request.method} {request_context.request.url}")
    else:
        print(f"Request success: {request_context.request.method} {request_context.request.url} - Status: {response.status_code}")


# ========================================
# EXECUÇÃO
# ========================================

if __name__ == "__main__":
    # Modo linha de comando
    import sys

    if "--headless" in sys.argv:
        # Modo headless (para CI/CD)
        pass
    else:
        # Modo interativo (com web UI)
        pass
