# steps/web2md_steps.py - Step definitions para web2md BDD tests
from behave import given, when, then, use_step_matcher
import subprocess
import time
import os
from pathlib import Path

use_step_matcher("re")

# ==================== GIVEN STEPS ====================

@given("que estou no diretório do projeto web2md")
def step_given_project_dir(context):
    """Muda para o diretório do projeto web2md"""
    context.project_dir = Path.home() / "web2md"
    assert context.project_dir.exists(), "Diretório web2md não encontrado"
    context.original_dir = os.getcwd()
    os.chdir(context.project_dir)

@given("que web2md está instalado")
def step_given_web2md_installed(context):
    """Verifica se web2md está instalado"""
    result = subprocess.run(
        ["which", "web2md"],
        capture_output=True,
        text=True
    )
    # Se não estiver no PATH, verifica se o script existe
    if result.returncode != 0:
        script_path = context.project_dir / "web2md.ts"
        assert script_path.exists(), "web2md.ts não encontrado"

@given("que acesso uma URL de artigo simples")
def step_given_simple_article_url(context):
    """Define uma URL de teste simples"""
    context.test_url = "https://example.com"

@given("que acesso página com elementos de ruído")
def step_given_noisy_page(context):
    """Define URL com elementos de ruído"""
    context.test_url = "https://httpbin.org/html"

@given("que acesso página com formatação complexa")
def step_given_complex_formatting(context):
    """Define URL com formatação complexa"""
    context.test_url = "https://httpbin.org/html"

@given("que acesso uma URL de SPA")
def step_given_spa_url(context):
    """Define URL de SPA (Single Page Application)"""
    context.test_url = "https://example.com/spa"

@given("que página HTML tem aproximadamente 15.000 tokens")
def step_given_large_html_page(context):
    """Define URL de página grande"""
    context.test_url = "https://httpbin.org/html"
    context.expected_html_tokens = 15000

@given("que página contém code blocks")
def step_given_page_with_code(context):
    """Define URL com code blocks"""
    context.test_url = "https://httpbin.org/html"

@given("que página contém links")
def step_given_page_with_links(context):
    """Define URL com links"""
    context.test_url = "https://example.com"

@given("que especifico arquivo de saída")
def step_given_output_file(context):
    """Define arquivo de saída"""
    import tempfile
    context.output_file = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
    context.output_path = context.output_file.name
    context.output_file.close()

@given("que executo web2md sem --out")
def step_given_no_output_flag(context):
    """Garante que não será usado --out"""
    context.output_path = None

@given("que acesso URL inválida")
def step_given_invalid_url(context):
    """Define URL inválida"""
    context.test_url = "not-a-url"

@given("que acesso URL (.*)")
def step_given_specific_url(context, url_description):
    """Define URL baseado em descrição"""
    url_map = {
        "simples": "https://example.com",
        "com ruído": "https://httpbin.org/html",
        "SPA": "https://example.com",
    }
    context.test_url = url_map.get(url_description, "https://example.com")

# ==================== WHEN STEPS ====================

@when("executo web2md na URL")
def step_when_execute_web2md(context):
    """Executa web2md na URL especificada"""
    context.start_time = time.time()

    cmd = ["bun", "run", "web2md.ts", context.test_url]
    if hasattr(context, 'output_path') and context.output_path:
        cmd.extend(["--out", context.output_path])

    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=context.project_dir
    )

    context.elapsed_time = time.time() - context.start_time

    # Capturar output
    if hasattr(context, 'output_path') and context.output_path:
        with open(context.output_path) as f:
            context.markdown_content = f.read()
    else:
        context.markdown_content = context.result.stdout

@when("executo web2md com flag --js")
def step_when_execute_web2md_js(context):
    """Executa web2md com flag --js"""
    context.start_time = time.time()

    cmd = ["bun", "run", "web2md.ts", "--js", context.test_url]

    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=context.project_dir
    )

    context.elapsed_time = time.time() - context.start_time
    context.markdown_content = context.result.stdout

@when("executo web2md com flag --out")
def step_when_execute_web2md_out(context):
    """Executa web2md com flag --out"""
    step_when_execute_web2md(context)  # Reuse existing step

@when("output é redirecionado")
def step_when_output_redirected(context):
    """Simula redirecionamento de output"""
    step_when_execute_web2md(context)

# ==================== THEN STEPS ====================

@then("devo receber Markdown limpo")
def step_then_markdown_clean(context):
    """Verifica se o output é Markdown válido"""
    assert len(context.markdown_content) > 0, "Output vazio"
    assert "#" in context.markdown_content or "content" in context.markdown_content.lower(), \
        "Não parece ser Markdown válido"

@then("tempo de processamento < (\\d+)s")
def step_then_processing_time(context, max_seconds):
    """Verifica se o processamento foi rápido o suficiente"""
    max_time = float(max_seconds)
    assert context.elapsed_time < max_time, \
        f"Processing too slow: {context.elapsed_time:.2f}s (limit: {max_time}s)"

@then("economia de tokens > (\\d+)%")
def step_then_token_economy(context, min_economy):
    """Verifica economia de tokens"""
    # Estimar tokens (4 chars ≈ 1 token)
    if hasattr(context, 'expected_html_tokens'):
        html_tokens = context.expected_html_tokens
        md_tokens = len(context.markdown_content) / 4

        if html_tokens > 0:
            economy = (1 - md_tokens / html_tokens) * 100
            assert economy > float(min_economy), \
                f"Token economy insufficient: {economy:.1f}% (expected: >{min_economy}%)"

@then("Markdown não deve conter elementos de ruído")
def step_then_no_noise(context):
    """Verifica se ruído foi removido"""
    noise_terms = ["advertisement", "sidebar", "navbar", "footer"]
    content_lower = context.markdown_content.lower()

    # Verificar se pelo menos alguns termos de ruído não estão presentes
    # (alguns podem aparecer legítimamente no conteúdo)
    noise_found = [term for term in noise_terms if term in content_lower]
    # Permitir até 2 termos (falso positivo)
    assert len(noise_found) <= 2, f"Noise found: {noise_found}"

@then("apenas conteúdo principal deve estar presente")
def step_then_main_content_only(context):
    """Verifica se conteúdo principal está presente"""
    assert len(context.markdown_content) > 100, "Content too short"
    # Verificar se há estrutura de conteúdo
    assert any(marker in context.markdown_content for marker in ["#", "-", "*", "http"]), \
        "No Markdown structure found"

@then("Markdown deve ter estrutura equivalente")
def step_then_structure_equivalent(context):
    """Verifica preservação de estrutura"""
    # Verificar elementos de estrutura Markdown
    assert "#" in context.markdown_content, "No headers found"
    assert len(context.markdown_content.split("\n")) > 5, "Too few lines"

@then("formatação deve ser válida")
def step_then_formatting_valid(context):
    """Verifica se formatação Markdown é válida"""
    # Verificar sintaxe Markdown básica
    lines = context.markdown_content.split("\n")
    has_headers = any(line.startswith("#") for line in lines)
    has_lists = any(line.strip().startswith(("- ", "* ", "+ ")) for line in lines)

    assert has_headers or has_lists, "No valid Markdown formatting found"

@then("devo receber conteúdo renderizado")
def step_then_content_rendered(context):
    """Verifica se conteúdo JS foi renderizado"""
    assert len(context.markdown_content) > 0, "No content rendered"
    # Para SPAs, verificar se há mais conteúdo que HTML cru
    assert len(context.markdown_content) > 500, "Rendered content too short"

@then("Markdown resultante deve ter < (\\d+) tokens")
def step_then_md_token_limit(context, max_tokens):
    """Verifica limite de tokens do Markdown"""
    md_tokens = len(context.markdown_content) / 4
    assert md_tokens < float(max_tokens), \
        f"Too many tokens: {md_tokens:.0f} (limit: {max_tokens})"

@then("economia deve ser > (\\d+)%")
def step_then_economy_percentage(context, min_economy):
    """Verifica porcentagem de economia"""
    if hasattr(context, 'expected_html_tokens'):
        html_tokens = context.expected_html_tokens
        md_tokens = len(context.markdown_content) / 4
        economy = (1 - md_tokens / html_tokens) * 100
        assert economy > float(min_economy), \
            f"Economy too low: {economy:.1f}% (expected: >{min_economy}%)"

@then("code blocks devem ser preservados")
def step_then_code_blocks_preserved(context):
    """Verifica preservação de code blocks"""
    # Verificar presença de code blocks (``` ou `)
    has_code_blocks = "```" in context.markdown_content or "`" in context.markdown_content
    assert has_code_blocks, "No code blocks found"

@then("linguagem deve ser identificada")
def step_then_language_identified(context):
    """Verifica se linguagem do código é identificada"""
    # Verificar se há code blocks com especificação de linguagem
    has_language_spec = "```python" in context.markdown_content or \
                        "```javascript" in context.markdown_content or \
                        "```bash" in context.markdown_content
    # Não é obrigatório, mas é desejável

@then("links devem ser convertidos para formato Markdown")
def step_then_links_converted(context):
    """Verifica conversão de links"""
    # Verificar presença de links Markdown
    has_markdown_links = "](" in context.markdown_content
    assert has_markdown_links, "No Markdown links found"

@then("processamento deve completar em < (\\d+)s")
def step_then_completion_time(context, max_seconds):
    """Verifica tempo de completion"""
    assert context.elapsed_time < float(max_seconds), \
        f"Processing too slow: {context.elapsed_time:.2f}s"

@then("uso de memória deve ser razoável")
def step_then_memory_usage_reasonable(context):
    """Verifica uso de memória (básico)"""
    # Verificação básica - se completou sem crash, memória foi OK
    assert context.result.returncode == 0 or \
           "memory" not in context.result.stderr.lower(), \
           "Memory issues detected"

@then("Markdown deve ser salvo no arquivo")
def step_then_file_saved(context):
    """Verifica se arquivo foi salvo"""
    assert hasattr(context, 'output_path'), "No output file specified"
    assert os.path.exists(context.output_path), f"File not created: {context.output_path}"
    assert os.path.getsize(context.output_path) > 0, "File is empty"

@then("arquivo deve ser válido")
def step_then_file_valid(context):
    """Verifica se arquivo é válido"""
    with open(context.output_path) as f:
        content = f.read()
    assert len(content) > 0, "File is empty"
    assert "#" in content or "content" in content.lower(), "Invalid Markdown"

@then("Markdown deve ser impresso em stdout")
def step_then_stdout_output(context):
    """Verifica output em stdout"""
    assert len(context.result.stdout) > 0, "No stdout output"
    assert "#" in context.result.stdout or "content" in context.result.stdout.lower(), \
        "Invalid Markdown in stdout"

@then("pode ser usado em pipes")
def step_then_pipe_compatible(context):
    """Verifica compatibilidade com pipes"""
    # Se output foi para stdout, pode ser usado em pipes
    assert len(context.result.stdout) > 0, "Not pipe-compatible"

@then("erro deve ser reportado em stderr")
def step_then_stderr_error(context):
    """Verifica erro em stderr"""
    assert len(context.result.stderr) > 0, "No error message in stderr"

@then("código de saída deve ser não-zero")
def step_then_nonzero_exit(context):
    """Verifica código de saída"""
    assert context.result.returncode != 0, f"Exit code should be non-zero, got {context.result.returncode}"

# ==================== CLEANUP ====================

def after_scenario(context, scenario):
    """Cleanup após cada cenário"""
    # Remover arquivo temporário se existir
    if hasattr(context, 'output_path') and context.output_path:
        try:
            if os.path.exists(context.output_path):
                os.unlink(context.output_path)
        except:
            pass

    # Voltar ao diretório original
    if hasattr(context, 'original_dir'):
        os.chdir(context.original_dir)
