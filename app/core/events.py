from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.api.routes import routers
from .config import get_app_settings
from .middleware.authentication import AuthenticationBackend
from .settings.base import BaseAppSettings, AppEnvTypes


def startup_handler(app: FastAPI):
    async def inner():
        configurate_db(app)

    return inner


def configurate_db(app: FastAPI):
    register_tortoise(
        app=app,
        config={
                'connections': {
                    'default': get_app_settings().DB_URI
                },
                'apps': {
                    'models': {
                        'models': ['app.models'],
                        'default_connection': 'default',
                    }
                }
            },
        generate_schemas=True
    )


def register_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router, prefix="/api/v1")


def use_authentication_middleware(app: FastAPI):
    app.add_middleware(
        AuthenticationMiddleware,
        backend=AuthenticationBackend()
    )


def use_production_settings() -> None:
    BaseAppSettings.app_env = AppEnvTypes.prod
