# dev-assist-mcp

**Idée de projet : DevAssist MCP**  
Un assistant de développement intelligent qui expose des outils via MCP pour automatiser les tâches répétitives du quotidien d'un développeur.

## Concept

Un serveur MCP connecté à une API FastAPI qui permet à Claude (ou tout LLM compatible) d'interagir avec l'environnement de développement : analyser du code, gérer des tâches, interroger une base de données de snippets, et générer de la documentation automatiquement.

## Les 4 modules du projet

1. **Snippet Manager** – CRUD de snippets avec tags et recherche (sémantique à venir). Outils MCP : `search_snippet`, `save_snippet`.
2. **Code Analyzer** – Analyse de code (complexité, bugs potentiels, suggestions). Outil MCP : `analyze_code`.
3. **Task Tracker** – Gestion de tâches par projet. Outils MCP : `create_task`, `list_tasks`.
4. **Doc Generator** – Génération de docstrings pour fonctions/classes Python. Outil MCP : `generate_docs`.

## Structure du projet

```
dev-assist-mcp/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .env.example
├── src/
│   └── dev_assist_mcp/
│       ├── __init__.py
│       ├── config.py           # Configuration (pydantic-settings)
│       ├── main.py             # Application FastAPI
│       ├── mcp_server.py       # Serveur MCP (outils list_tools / call_tool)
│       └── modules/
│           ├── snippet_manager/   # models, service, api
│           ├── code_analyzer/     # service, api
│           ├── task_tracker/      # models, service, api
│           └── doc_generator/     # service, api
├── scripts/
│   ├── run_api.sh             # Lance l’API (uvicorn)
│   └── run_mcp.sh             # Lance le serveur MCP (stdio)
└── tests/
    ├── test_snippet_service.py
    └── test_code_analyzer.py
```

## Démarrer

### Environnement

```bash
python -m venv .venv
source .venv/bin/activate   # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt
# Optionnel : copier .env.example vers .env
```

### Lancer l’API FastAPI

```bash
export PYTHONPATH=src
uvicorn dev_assist_mcp.main:app --reload --port 8000
# ou : ./scripts/run_api.sh
```

- Doc : http://localhost:8000/docs  
- Health : http://localhost:8000/health  

### Lancer le serveur MCP

Requis : **Python 3.10+** et `pip install -r requirements-mcp.txt` (ou `pip install mcp`).

À configurer dans Cursor/Claude comme serveur MCP (stdio) :

```bash
export PYTHONPATH=src
python -m dev_assist_mcp.mcp_server
# ou : ./scripts/run_mcp.sh
```

### Tests

```bash
pip install -e ".[dev]"
pytest
```
