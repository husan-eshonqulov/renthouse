from typing import Literal

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    postgres_url: PostgresDsn
    redis_url: RedisDsn
    python_env: Literal["development", "production"]

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()  # type: ignore
