"""Routes FastAPI pour le Snippet Manager."""

from fastapi import APIRouter, HTTPException

from dev_assist_mcp.modules.snippet_manager.models import SnippetCreate, SnippetResponse, SnippetSearchQuery
from dev_assist_mcp.modules.snippet_manager.service import snippet_service

router = APIRouter()


@router.post("/", response_model=SnippetResponse)
async def create_snippet(data: SnippetCreate):
    """Crée un snippet."""
    sid = await snippet_service.save_and_return_id(
        title=data.title,
        content=data.content,
        tags=data.tags,
    )
    snippet = await snippet_service.get(sid)
    if not snippet:
        raise HTTPException(status_code=500, detail="Création OK mais récupération échouée")
    return SnippetResponse(**snippet)


@router.get("/search")
async def search_snippets(query: str, limit: int = 10):
    """Recherche des snippets."""
    text = await snippet_service.search(query=query, limit=limit)
    return {"results": text}


@router.get("/{snippet_id}")
async def get_snippet(snippet_id: str):
    """Récupère un snippet par id."""
    snippet = await snippet_service.get(snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet non trouvé")
    return snippet
