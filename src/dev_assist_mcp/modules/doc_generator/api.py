"""Routes FastAPI pour le Doc Generator."""

from fastapi import APIRouter
from pydantic import BaseModel

from dev_assist_mcp.modules.doc_generator.service import generate_docs

router = APIRouter()


class GenerateDocsRequest(BaseModel):
    """Requête de génération de documentation."""
    code: str


@router.post("/")
async def generate_docs_endpoint(req: GenerateDocsRequest):
    """Génère la documentation (docstrings) pour le code Python fourni."""
    result = await generate_docs(code=req.code)
    return {"documentation": result}
