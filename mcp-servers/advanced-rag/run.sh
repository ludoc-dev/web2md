#!/bin/bash
# Wrapper script para Advanced RAG MCP Server
cd "$(dirname "$0")"
source venv/bin/activate
python -u server.py
