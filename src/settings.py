from typing import Literal

from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    python_env: Literal["development", "production"]
    bot_token: str
    postgres_url: PostgresDsn
    redis_url: RedisDsn

    domain_name: str | None = None

    model_config = SettingsConfigDict(extra="ignore")

    @model_validator(mode="after")
    def validate_production_fields(self):
        if self.python_env == "production":
            missing: list[str] = []

            if self.domain_name is None:
                missing.append("web_server_domain")
            if missing:
                raise ValueError(f"Missing required production fields: {missing}")

        return self


settings = Settings()  # type: ignore
