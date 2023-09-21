from enum import StrEnum

from pydantic_settings import BaseSettings


class AppEnvTypes(StrEnum):
    prod = "prod"
    dev = "dev"
    test = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.dev

    class Config:
        env_file = ".env"
