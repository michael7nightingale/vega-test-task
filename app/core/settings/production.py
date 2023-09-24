from .base import BaseAppSettings


class ProdAppSettings(BaseAppSettings):
    LOGGING_LEVEL: str = "ERROR"
    DEBUG: bool = False
    DB_URI: str

    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int

    FILES_DIR: str = "app/files/"

    class Config:
        env_file = "prod.env"
