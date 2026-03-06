#!/usr/bin/env bash
# Lance l'API FastAPI DevAssist (depuis la racine du projet)
set -e
cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}src"
uvicorn dev_assist_mcp.main:app --reload --host 0.0.0.0 --port 8000
