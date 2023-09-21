from fastapi import APIRouter, Body, Request

from schemas.users import UpdateUserSchema, LoginUserSchema, RegisterUserSchema


router = APIRouter(prefix="/users")


@router.post("/register")
async def register(register_data: RegisterUserSchema = Body()):
    return


@router.post("/login")
async def login(login_data: LoginUserSchema = Body()):
    return


@router.get("/me/data")
async def me_profile(request: Request):
    return request.user


@router.patch("/me/data")
async def me_profile_update(request: Request, update_data: UpdateUserSchema = Body()):
    return


@router.get("/me/companies")
async def me_companies(request: Request):
    return


@router.get("/me/settings")
async def me_settings(request: Request):
    return
