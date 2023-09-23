from fastapi import HTTPException, Request

from app.models.watches import Watch, Task
from app.services.authentication import login_required


@login_required
async def get_watch(request: Request, watch_id: str):
    watch = await Watch.get_or_none(id=watch_id, user=request.user)
    if watch is None:
        raise HTTPException(
            detail=f"Watch {watch_id} for user with id={request.user.id} does not exist.",
            status_code=404
        )
    if not watch.is_watched:
        watch.is_watched = True
        await watch.save()
    return watch


@login_required
async def get_task(request: Request, watch_id: str, task_id: str):
    task = await Task.get_or_none(id=task_id, watch__user=request.user, watch_id=watch_id)
    if task is None:
        raise HTTPException(
            detail=f"Task {task_id} for user with id={request.user.id} does not exist.",
            status_code=404
        )
    return task
