from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OPENAI_")

    api_key: str = "sk-fake"
    model: str = "gpt-4o-mini"
    timeout_seconds: float = 30.0
