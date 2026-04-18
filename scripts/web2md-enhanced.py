#!/usr/bin/env python3
"""
web2md-enhanced.py - web2md com backend Trafilatura
Combina flexibilidade do web2md com robustez do Trafilatura
"""

import sys
import trafilatura
import subprocess
from pathlib import Path

def web2md_with_fallback(url: str, use_js: bool = False) -> str:
    """
    Extrai conteúdo para Markdown usando web2md ou Trafilatura
    
    Args:
        url: URL para extrair
        use_js: Se True, usa --js flag
    
    Returns:
        Conteúdo em Markdown
    """
    
    # Tentar web2md primeiro (mais rápido para casos simples)
    try:
        print(f"[INFO] Tentando web2md para {url}...", file=sys.stderr)
        
        cmd = ["bun", "run", "web2md.ts"]
        if use_js:
            cmd.append("--js")
        cmd.append(url)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=Path(__file__).parent.parent
        )
        
        if result.returncode == 0 and len(result.stdout) > 100:
            print(f"[INFO] web2md sucesso: {len(result.stdout)} chars", file=sys.stderr)
            return result.stdout
        
        print(f"[WARN] web2md falhou, usando Trafilatura...", file=sys.stderr)
        
    except Exception as e:
        print(f"[WARN] web2md erro: {e}, usando Trafilatura...", file=sys.stderr)
    
    # Fallback para Trafilatura (mais robusto)
    try:
        print(f"[INFO] Usando Trafilatura para {url}...", file=sys.stderr)
        
        # Fetch URL
        downloaded = trafilatura.fetch_url(url)
        
        # Extract to markdown
        content = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            output_format="markdown",
            url=url
        )
        
        if content and len(content) > 100:
            print(f"[INFO] Trafilatura sucesso: {len(content)} chars", file=sys.stderr)
            return content
        
        raise Exception("Conteúdo muito curto ou vazio")
        
    except Exception as e:
        print(f"[ERROR] Trafilatura também falhou: {e}", file=sys.stderr)
        raise

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Usage: web2md-enhanced.py <URL> [--js]")
        print("\nExemplo:")
        print("  python web2md-enhanced.py https://example.com")
        print("  python web2md-enhanced.py https://example.com --js")
        sys.exit(1)
    
    url = sys.argv[1]
    use_js = "--js" in sys.argv
    
    try:
        markdown = web2md_with_fallback(url, use_js)
        print(markdown)
        
    except Exception as e:
        print(f"Erro fatal: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
