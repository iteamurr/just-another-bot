from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    debug: bool = False
    backend_url: str = "http://localhost:8000"
