"""Modèles Pydantic et données pour les snippets."""

from pydantic import BaseModel
from typing import Optional


class SnippetCreate(BaseModel):
    """Création d'un snippet."""
    title: str
    content: str
    tags: list[str] = []


class SnippetResponse(BaseModel):
    """Snippet renvoyé par l'API."""
    id: str
    title: str
    content: str
    tags: list[str]

    class Config:
        from_attributes = True


class SnippetSearchQuery(BaseModel):
    """Requête de recherche."""
    query: str
    limit: int = 10
