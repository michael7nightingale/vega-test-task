from functools import lru_cache

from .settings.base import BaseAppSettings, AppEnvTypes
from app.core.settings.development import DevAppSettings
from app.core.settings.production import ProdAppSettings
from app.core.settings.test import TestAppSettings


environments = {
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
    AppEnvTypes.dev: DevAppSettings,

}


@lru_cache
def get_app_settings() -> BaseAppSettings:
    env_type = BaseAppSettings().app_env
    settings_cls = environments[env_type]
    return settings_cls()
