import os
from pathlib import Path

from pydantic import BaseSettings
from pydantic.tools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if os.path.exists(str(BASE_DIR / ".env")):
    ENV_FILE = ".env"
else:
    ENV_FILE = ".env.example"


class Settings(BaseSettings):
    """Настройки проекта."""

    DEBUG: bool = False

    class Config:
        env_file = ENV_FILE


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
