# features/environment.py - Configuração do ambiente Behave
from behave import use_step_matcher
import os
import tempfile
from pathlib import Path

def before_all(context):
    """Setup antes de todos os testes"""
    context.config.setup_logging()

    # Diretório do projeto
    context.project_dir = Path.home() / "web2md"

    # Diretório temporário para testes
    context.temp_dir = tempfile.mkdtemp(prefix="web2md_test_")

    # Configurações
    context.config.userdata.setdefault("timeout", 30)
    context.config.userdata.setdefault("base_url", "https://example.com")

def after_all(context):
    """Cleanup após todos os testes"""
    import shutil
    if hasattr(context, 'temp_dir') and os.path.exists(context.temp_dir):
        shutil.rmtree(context.temp_dir)

def before_scenario(context, scenario):
    """Setup antes de cada cenário"""
    # Criar environment para o cenário
    context.scenario_start_time = __import__("time").time()
    context.scenario_temp_dir = tempfile.mkdtemp(prefix=f"scenario_{scenario.name}_")

def after_scenario(context, scenario):
    """Cleanup após cada cenário"""
    import shutil
    import os

    # Remover diretório temporário do cenário
    if hasattr(context, 'scenario_temp_dir') and os.path.exists(context.scenario_temp_dir):
        shutil.rmtree(context.scenario_temp_dir)

    # Log de tempo do cenário
    if hasattr(context, 'scenario_start_time'):
        elapsed = __import__("time").time() - context.scenario_start_time
        print(f"\n⏱️  Scenario duration: {elapsed:.2f}s")
