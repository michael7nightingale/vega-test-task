from fastapi import APIRouter, Body, Request

from app.schemas.users import UpdateUserSchema, LoginUserSchema, RegisterUserSchema


router = APIRouter(prefix="/users")


@router.post("/register")
async def register(register_data: RegisterUserSchema = Body()):
    return


@router.post("/login")
async def login(login_data: LoginUserSchema = Body()):
    return


@router.get("/me/data")
# @login_required
async def me_profile(request: Request):
    return request.user


@router.patch("/me/data")
# @login_required
async def me_profile_update(request: Request, update_data: UpdateUserSchema = Body()):
    return


@router.get("/me/companies")
# @login_required
async def me_companies(request: Request):
    return


@router.get("/me/settings")
# @login_required
async def me_settings(request: Request):
    return


@router.patch("/me/settings")
# @login_required
async def me_settings_update(request: Request):
    return
