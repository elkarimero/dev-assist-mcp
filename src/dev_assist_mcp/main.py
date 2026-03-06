"""Point d'entrée FastAPI - DevAssist MCP."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from dev_assist_mcp.config import settings
from dev_assist_mcp.modules.snippet_manager.api import router as snippet_router
from dev_assist_mcp.modules.code_analyzer.api import router as analyzer_router
from dev_assist_mcp.modules.task_tracker.api import router as task_router
from dev_assist_mcp.modules.doc_generator.api import router as doc_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialisation au démarrage, nettoyage à l'arrêt."""
    # TODO: init DB, modèles d'embeddings, etc.
    yield
    # TODO: fermeture connexions


app = FastAPI(
    title="DevAssist MCP API",
    description="API pour Snippet Manager, Code Analyzer, Task Tracker, Doc Generator",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(snippet_router, prefix="/api/snippets", tags=["Snippets"])
app.include_router(analyzer_router, prefix="/api/analyze", tags=["Code Analyzer"])
app.include_router(task_router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(doc_router, prefix="/api/docs", tags=["Doc Generator"])


@app.get("/health")
def health():
    """Santé de l'API."""
    return {"status": "ok"}


def run_api():
    """Lance le serveur API (pour usage en script)."""
    import uvicorn
    uvicorn.run(
        "dev_assist_mcp.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )


if __name__ == "__main__":
    run_api()
