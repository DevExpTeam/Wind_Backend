import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from enum import Enum


class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings, extra='ignore'):
    PROJECT_NAME: str = "app"
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    MODE: ModeEnum = ModeEnum.development 

    
    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("../../.env")


settings = Settings()
