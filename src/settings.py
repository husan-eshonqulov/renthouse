from typing import Literal

from pydantic import HttpUrl, PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    python_env: Literal["development", "production"] = "development"

    bot_token: str
    postgres_url: PostgresDsn
    redis_url: RedisDsn

    web_server_host: str | None = None
    web_server_port: int | None = None
    webhook_path: str | None = None
    base_webhook_url: HttpUrl | None = None

    model_config = SettingsConfigDict(extra="ignore")

    @model_validator(mode="after")
    def validate_production_fields(self):
        if self.python_env == "production":
            missing: list[str] = []

            if self.web_server_host is None:
                missing.append("web_server_host")
            if self.web_server_port is None:
                missing.append("web_server_port")
            if self.webhook_path is None:
                missing.append("webhook_path")
            if self.base_webhook_url is None:
                missing.append("base_webhook_url")

            if missing:
                raise ValueError(f"Missing required production fields: {missing}")

        return self


settings = Settings()  # type: ignore
