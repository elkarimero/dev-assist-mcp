"""Routes FastAPI pour le Code Analyzer."""

from fastapi import APIRouter
from pydantic import BaseModel

from dev_assist_mcp.modules.code_analyzer.service import analyze_code

router = APIRouter()


class AnalyzeRequest(BaseModel):
    """Requête d'analyse de code."""
    code: str
    language: str = "python"


@router.post("/")
async def analyze_code_endpoint(req: AnalyzeRequest):
    """Analyse le code et retourne complexité, bugs potentiels, suggestions."""
    result = await analyze_code(code=req.code, language=req.language)
    return {"analysis": result}
