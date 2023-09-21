from fastapi import FastAPI

from core.events import startup_handler, register_routers, use_authentication_middleware


def create_app() -> FastAPI:
    app = FastAPI()
    register_routers(app)
    use_authentication_middleware(app)
    app.add_event_handler("startup", startup_handler(app))
    return app
