from .base import BaseAppSettings


class DevAppSettings(BaseAppSettings):

    LOGGING_LEVEL: str = "INFO"
    DEBUG: bool = True
    DB_URI: str

    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_MINUTES: int

    FILES_DIR: str = "app/files/"

    class Config:
        env_file = "dev.env"
