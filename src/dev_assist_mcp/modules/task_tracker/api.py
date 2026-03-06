"""Routes FastAPI pour le Task Tracker."""

from typing import Optional

from fastapi import APIRouter, HTTPException

from dev_assist_mcp.modules.task_tracker.models import TaskCreate, TaskResponse
from dev_assist_mcp.modules.task_tracker.service import task_service

router = APIRouter()


@router.post("/", response_model=TaskResponse)
async def create_task(data: TaskCreate):
    """Crée une tâche."""
    tid = await task_service.create_and_return_id(
        title=data.title,
        description=data.description,
        project=data.project,
    )
    task = await task_service.get(tid)
    if not task:
        raise HTTPException(status_code=500, detail="Création OK mais récupération échouée")
    return TaskResponse(**task)


@router.get("/")
async def list_tasks(project: Optional[str] = None, status: Optional[str] = None, limit: int = 20):
    """Liste les tâches."""
    tasks = await task_service.get_all(project=project, status=status, limit=limit)
    return {"tasks": tasks}


@router.get("/{task_id}")
async def get_task(task_id: str):
    """Récupère une tâche par id."""
    task = await task_service.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return task


@router.patch("/{task_id}")
async def update_task_status(task_id: str, status: str):
    """Met à jour le statut (open, in_progress, done)."""
    ok = await task_service.update_status(task_id, status)
    if not ok:
        raise HTTPException(status_code=400, detail="Tâche non trouvée ou statut invalide")
    return await task_service.get(task_id)
