from .base import BaseAppSettings


class TestAppSettings(BaseAppSettings):
    LOGGING_LEVEL: str = "INFO"
    DEBUG: bool = False
    DB_URI: str

    SECRET_KEY: str = "12309182903"
    ALGORITHM: str = "HS256"
    EXPIRE_MINUTES: int = 100

    class Config:
        env_file = "test.env"
