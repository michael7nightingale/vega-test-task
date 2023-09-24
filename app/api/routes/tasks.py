from fastapi import APIRouter, Request, Body, Depends

from app.api.dependencies.watches import get_watch
from app.api.dependencies.tasks import get_task
from app.models import Watch, Task
from app.schemas.tasks import TaskSchema, TaskUpdateSchema, TaskCreateSchema
from app.services.authentication import login_required


router = APIRouter(prefix="/tasks")


@router.get("/{watch_id}", response_model=list[TaskSchema])
@login_required
async def get_watch_tasks(
        request: Request,
        watch: Watch = Depends(get_watch)
):
    return await watch.tasks.all()


@router.post("/{watch_id}", response_model=list[TaskSchema])
@login_required
async def create_watch_tasks(
        request: Request,
        watch: Watch = Depends(get_watch),
        task_data_list: list[TaskCreateSchema] = Body()
):
    return await Task.bulk_create(
        [
            Task(**task_data.model_dump(), watch=watch) for task_data in task_data_list
        ]
    )


@router.patch("/{watch_id}/{task_id}/refuse", response_model=TaskSchema)
@login_required
async def refuse_task(
        request: Request,
        task: Task = Depends(get_task),
):
    await task.refuse()
    return task


@router.patch("/{watch_id}/{task_id}/finish", response_model=TaskSchema)
@login_required
async def refuse_task(
        request: Request,
        task: Task = Depends(get_task),
):
    await task.finish()
    return task
