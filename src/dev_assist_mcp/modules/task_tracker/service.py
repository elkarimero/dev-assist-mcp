"""Logique Task Tracker (stockage en mémoire pour le squelette)."""

import uuid
from typing import Optional

_tasks: dict[str, dict] = {}
_statuses = ("open", "in_progress", "done")


class TaskService:
    """Service de gestion des tâches."""

    async def create(
        self,
        title: str,
        description: str = "",
        project: str = "default",
    ) -> str:
        """Crée une tâche et retourne un message pour MCP."""
        tid = str(uuid.uuid4())
        _tasks[tid] = {
            "id": tid,
            "title": title,
            "description": description,
            "project": project,
            "status": "open",
        }
        return f"Tâche créée : id={tid}, title={title!r}, project={project!r}"

    async def create_and_return_id(
        self,
        title: str,
        description: str = "",
        project: str = "default",
    ) -> str:
        """Crée une tâche et retourne son id (pour l'API REST)."""
        tid = str(uuid.uuid4())
        _tasks[tid] = {
            "id": tid,
            "title": title,
            "description": description,
            "project": project,
            "status": "open",
        }
        return tid

    async def list_tasks(
        self,
        project: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> str:
        """Liste les tâches (pour MCP : retour texte)."""
        filtered = list(_tasks.values())
        if project:
            filtered = [t for t in filtered if t["project"] == project]
        if status:
            filtered = [t for t in filtered if t["status"] == status]
        filtered = filtered[:limit]
        if not filtered:
            return "Aucune tâche trouvée."
        lines = [
            f"- [{t['title']}] id={t['id']} project={t['project']} status={t['status']}"
            for t in filtered
        ]
        return "\n".join(lines)

    async def get_all(
        self,
        project: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> list[dict]:
        """Liste les tâches (pour l'API REST : liste d'objets)."""
        filtered = list(_tasks.values())
        if project:
            filtered = [t for t in filtered if t["project"] == project]
        if status:
            filtered = [t for t in filtered if t["status"] == status]
        return filtered[:limit]

    async def get(self, task_id: str) -> Optional[dict]:
        """Récupère une tâche par id."""
        return _tasks.get(task_id)

    async def update_status(self, task_id: str, status: str) -> bool:
        """Met à jour le statut d'une tâche."""
        if task_id not in _tasks or status not in _statuses:
            return False
        _tasks[task_id]["status"] = status
        return True


task_service = TaskService()
