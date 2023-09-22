from fastapi import FastAPI
import os

from app.core.events import (
    startup_handler,
    register_routers,
    use_authentication_middleware,
    use_production_settings,

)


def create_app(*args, **kwargs) -> FastAPI:
    """Application factory function."""
    app = FastAPI()

    if os.getenv("PROD"):   # checks if to use production environment
        use_production_settings()

    register_routers(app)
    use_authentication_middleware(app)
    app.add_event_handler("startup", startup_handler(app))

    return app
