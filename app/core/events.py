from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from core.config import get_app_settings


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
                        'models': ['models'],
                        'default_connection': 'default',
                    }
                }
            },
        generate_schemas=True
    )
