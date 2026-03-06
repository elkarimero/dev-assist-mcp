"""Modèles pour les tâches."""

from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    """Création d'une tâche."""
    title: str
    description: str = ""
    project: str = "default"


class TaskResponse(BaseModel):
    """Tâche renvoyée par l'API."""
    id: str
    title: str
    description: str
    project: str
    status: str

    class Config:
        from_attributes = True
