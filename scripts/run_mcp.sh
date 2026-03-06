#!/usr/bin/env bash
# Lance le serveur MCP DevAssist (stdio, pour Claude / Cursor)
set -e
cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}src"
python -m dev_assist_mcp.mcp_server
