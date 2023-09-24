from fastapi import Request, HTTPException

from app.models import Task
from app.services.authentication import login_required


@login_required
async def get_task(request: Request, task_id: str, watch_id: str):
    task = await Task.get_or_none(id=task_id, watch__user=request.user, watch_id=watch_id)
    if task is None:
        raise HTTPException(
            detail=f"Task {task_id} for user with id={request.user.id} does not exist.",
            status_code=404
        )
    return task
