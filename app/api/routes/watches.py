from fastapi import APIRouter, Request, Body, Depends

from app.models.watches import Watch
from app.services.authentication import login_required
from app.schemas.watches import (
    WatchSchema, WatchUpdateSchema, WatchRefuseSchema, WatchFinishSchema, WatchCreateSchema, WatchListSchema,
    ContactPersonSchema, ContactPersonUpdateSchema, ContactPersonCreateSchema,

)
from app.api.dependencies.watches import get_watch


router = APIRouter(prefix="/watches")


@router.get("/", response_model=list[WatchListSchema])
@login_required
async def get_watches(request: Request):
    return await request.user.watches.all()


@router.post("/", response_model=WatchSchema)
@login_required
async def create_watch(
        request: Request,
        watch_data: WatchCreateSchema = Body(),
):
    watch = await Watch.create(**watch_data.model_dump(), user=request.user)
    return WatchSchema(**watch.as_dict())


@router.get("/{watch_id}", response_model=WatchSchema)
@login_required
async def get_watch_detail(request: Request, watch: Watch = Depends(get_watch)):
    return watch


@router.patch("/{watch_id}", response_model=WatchSchema)
@login_required
async def update_watch(
        request: Request,
        watch_update_data: WatchUpdateSchema = Body(),
        watch: Watch = Depends(get_watch)
):
    await watch.update_from_dict(watch_update_data.model_dump())
    await watch.save()
    return watch


@router.patch("/{watch_id}/refuse", response_model=WatchSchema)
@login_required
async def watch_refuse(
        request: Request,
        watch_refuse_data: WatchRefuseSchema = Body(),
        watch: Watch = Depends(get_watch)
):
    await watch.refuse(**watch_refuse_data.model_dump())
    return watch


@router.patch("/{watch_id}/finish", response_model=WatchSchema)
@login_required
async def watch_finish(
        request: Request,
        watch_finish_data: WatchFinishSchema = Body(),
        watch: Watch = Depends(get_watch)
):
    await watch.finish(**watch_finish_data.model_dump())
    return watch


@router.post("/{watch_id}/contact-persons", response_model=list[ContactPersonSchema])
@login_required
async def create_watch_contact_persons(
        request: Request,
        contact_person_data_list: list[ContactPersonCreateSchema] = Body(),
        watch: Watch = Depends(get_watch)
):
    contact_persons_instances = await watch.save_contacts([i.model_dump() for i in contact_person_data_list])
    return contact_persons_instances
