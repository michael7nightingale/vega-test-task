from fastapi import FastAPI

from core.events import startup_handler


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_event_handler("startup", startup_handler(app))

    return app
