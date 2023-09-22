from fastapi import APIRouter, Request, Body, Depends
from fastapi.responses import JSONResponse

from app.models.watches import Watch
from app.services.authentication import login_required
from app.schemas.watches import (
    WatchSchema, WatchUpdateSchema, WatchRefuseSchema, WatchFinishSchema,
    ContactPersonSchema, ContactPersonUpdateSchema,
    TaskSchema, TaskUpdateSchema,
    ObjectSchema, ObjectUpdateSchema,

)
from app.api.dependencies.watches import get_watch


router = APIRouter(prefix="/watches")


@router.get("/", response_model=list[WatchSchema])
@login_required
async def get_watches(request: Request):
    return request.user.watches.all()


@router.get("/{watch_id}", response_model=WatchSchema)
@login_required
async def get_watch_detail(request: Request, watch: Watch = Depends(get_watch)):
    return watch


@router.patch("/{watch_id}", response_model=WatchSchema)
@login_required
async def get_watch_update(
        request: Request,
        watch_update_data: WatchUpdateSchema = Body(),
        watch: Watch = Depends(get_watch)
):
    await watch.update_from_dict(watch_update_data.model_dump())
    await watch.save()
    return watch


@router.patch("/{watch_id}/refuse", response_model=WatchSchema)
@login_required
async def get_watch_refuse(
        request: Request,
        watch_refuse_data: WatchRefuseSchema = Body(),
        watch: Watch = Depends(get_watch)
):
    await watch.refuse(**watch_refuse_data.model_dump())
    return watch


@router.patch("/{watch_id}/finish", response_model=WatchSchema)
@login_required
async def get_watch_finish(
        request: Request,
        watch_finish_data: WatchFinishSchema = Body(),
        watch: Watch = Depends(get_watch)
):
    await watch.finish(**watch_finish_data.model_dump())
    return watch


@router.get("/{watch_id}/tasks", response_model=list[TaskSchema])
@login_required
async def get_watch_tasks(
        request: Request,
        watch: Watch = Depends(get_watch)
):
    return await watch.tasks.all()
