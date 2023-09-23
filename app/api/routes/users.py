from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse

from app.schemas.companies import CompanySchema
from app.schemas.users import (
    UpdateUserSchema, UserSchema,
    LoginUserSchema, RegisterUserSchema,
    UserSettingsUpdateSchema, UserSettingsSchema,

)
from app.models.users import User
from app.services.authentication import encode_jwt_token, login_required


router = APIRouter(prefix="/users")


@router.post("/register", response_model=UserSchema)
async def register(register_data: RegisterUserSchema = Body()):
    """User register endpoint."""
    new_user = await User.register(**register_data.model_dump(exclude={"confirm_password"}))
    if new_user is None:
        return JSONResponse(
            content={
                "detail": "User with such data already exists.",
            },
            status_code=400
        )
    return new_user


@router.post("/token")
async def token_login(login_data: LoginUserSchema = Body()):
    """User login (getting access token) endpoint."""
    user = await User.login(**login_data.model_dump(exclude={"confirm_password", "login"}))
    if user is None:
        return JSONResponse(
            content={
                "detail": "Auth credentials are invalid.",
            },
            status_code=400
        )
    return {"access-token": encode_jwt_token(user.id)}


@router.get("/me/data", response_model=UserSchema)
@login_required
async def me_profile(request: Request):
    """Getting current user data endpoint."""
    return request.user


@router.patch("/me/data", response_model=UserSchema)
@login_required
async def me_profile_update(request: Request, update_data: UpdateUserSchema = Body()):
    """Updating current user data endpoint."""
    return


@router.get("/me/settings", response_model=UserSettingsSchema)
@login_required
async def me_settings(request: Request):
    """Getting current user settings endpoint."""
    user = await User.first()
    return await user.get_settings()


@router.patch("/me/settings")
@login_required
async def me_settings_update(request: Request, user_settings_data: UserSettingsUpdateSchema = Body()):
    """Updating current user settings endpoint."""
    user = await User.first()
    settings = await user.get_settings()
    await settings.update_from_dict(user_settings_data.model_dump())
    await settings.save()
    return settings


@router.get("/me/companies", response_model=list[CompanySchema])
@login_required
async def me_companies(request: Request):
    """Getting current user companies list endpoint."""
    return request.user.get_companies()
