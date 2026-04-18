#!/bin/bash
# Wrapper script para Code Graph MCP Server
cd "$(dirname "$0")"
source venv/bin/activate
python -u server.py
