from fastapi import APIRouter, Request, Body, Depends

from app.models import Object, Watch
from app.api.dependencies.objects import get_object
from app.api.dependencies.watches import get_watch
from app.services.authentication import login_required
from app.schemas.objects import ObjectCreateSchema, ObjectSchema, ObjectUpdateSchema


router = APIRouter(prefix="/objects")


@router.get("/{watch_id}", response_model=list[ObjectSchema])
@login_required
async def get_watch_objects(
        request: Request,
        watch: Watch = Depends(get_watch)
):
    return await watch.objects.all()


@router.post("/{watch_id}", response_model=list[ObjectSchema])
@login_required
async def create_watch_objects(
        request: Request,
        objects_data: list[ObjectCreateSchema] = Body(),
        watch: Watch = Depends(get_watch)
):
    objects_instances = await watch.save_objects([i.model_dump() for i in objects_data])
    return objects_instances


@router.patch("/{watch_id}/{objects_id}", response_model=ObjectSchema)
@login_required
async def create_watch_objects(
        request: Request,
        objects_update_data: ObjectUpdateSchema = Body(),
        object_: Object = Depends(get_object)
):
    await object_.update_from_dict(objects_update_data.model_dump())
    return object_


@router.patch("/{watch_id}/{objects_id}", response_model=ObjectSchema)
@login_required
async def create_watch_objects(
        request: Request,
        objects_update_data: ObjectUpdateSchema = Body(),
        object_: Object = Depends(get_object)
):
    await object_.update_from_dict(objects_update_data.model_dump())
    return object_


@router.patch("/{watch_id}/{objects_id}/watch", response_model=ObjectSchema)
@login_required
async def create_watch_objects(
        request: Request,
        object_: Object = Depends(get_object)
):
    await object_.watch()
    return object_
