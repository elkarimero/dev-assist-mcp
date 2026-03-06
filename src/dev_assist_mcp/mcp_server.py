"""Serveur MCP exposant les outils DevAssist. Requiert Python 3.10+ et pip install mcp."""

import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from dev_assist_mcp.modules.snippet_manager.service import snippet_service
from dev_assist_mcp.modules.code_analyzer.service import analyze_code as analyze_code_impl
from dev_assist_mcp.modules.task_tracker.service import task_service
from dev_assist_mcp.modules.doc_generator.service import generate_docs as generate_docs_impl


app = Server("dev-assist-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Liste les outils MCP exposés par DevAssist."""
    return [
        Tool(
            name="search_snippet",
            description="Recherche des snippets de code par requête textuelle ou tags. Retourne les snippets correspondants.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Requête de recherche ou tags séparés par des virgules"},
                    "limit": {"type": "integer", "description": "Nombre max de résultats", "default": 10},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="save_snippet",
            description="Enregistre un nouveau snippet de code avec titre, contenu et tags optionnels.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Titre du snippet"},
                    "content": {"type": "string", "description": "Contenu du code"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags optionnels"},
                },
                "required": ["title", "content"],
            },
        ),
        Tool(
            name="analyze_code",
            description="Analyse du code : complexité, bugs potentiels, suggestions d'amélioration.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Code source à analyser"},
                    "language": {"type": "string", "description": "Langage (python, js, etc.)", "default": "python"},
                },
                "required": ["code"],
            },
        ),
        Tool(
            name="create_task",
            description="Crée une tâche liée à un projet (titre, description, projet optionnel).",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Titre de la tâche"},
                    "description": {"type": "string", "description": "Description optionnelle"},
                    "project": {"type": "string", "description": "Nom du projet"},
                },
                "required": ["title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="Liste les tâches, optionnellement filtrées par projet ou statut.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Filtrer par projet"},
                    "status": {"type": "string", "description": "Filtrer par statut (open, done, etc.)"},
                    "limit": {"type": "integer", "description": "Nombre max de tâches", "default": 20},
                },
            },
        ),
        Tool(
            name="generate_docs",
            description="Génère la documentation (docstring) d'une fonction ou classe Python à partir du code source.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Code source Python (fonction ou classe)"},
                },
                "required": ["code"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Dispatch des appels vers les implémentations des modules."""
    if name == "search_snippet":
        result = await snippet_service.search(
            query=arguments["query"],
            limit=arguments.get("limit", 10),
        )
        return [TextContent(type="text", text=result)]

    if name == "save_snippet":
        result = await snippet_service.save(
            title=arguments["title"],
            content=arguments["content"],
            tags=arguments.get("tags") or [],
        )
        return [TextContent(type="text", text=result)]

    if name == "analyze_code":
        result = await analyze_code_impl(
            code=arguments["code"],
            language=arguments.get("language", "python"),
        )
        return [TextContent(type="text", text=result)]

    if name == "create_task":
        result = await task_service.create(
            title=arguments["title"],
            description=arguments.get("description", ""),
            project=arguments.get("project", "default"),
        )
        return [TextContent(type="text", text=result)]

    if name == "list_tasks":
        result = await task_service.list_tasks(
            project=arguments.get("project"),
            status=arguments.get("status"),
            limit=arguments.get("limit", 20),
        )
        return [TextContent(type="text", text=result)]

    if name == "generate_docs":
        result = await generate_docs_impl(code=arguments["code"])
        return [TextContent(type="text", text=result)]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def run_mcp_server():
    """Lance le serveur MCP en stdio (pour intégration Claude/LLM)."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    """Point d'entrée CLI pour le serveur MCP."""
    asyncio.run(run_mcp_server())


if __name__ == "__main__":
    main()
