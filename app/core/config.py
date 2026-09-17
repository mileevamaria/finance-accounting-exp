from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # JWT
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    token_algorithm: str = 'HS256'

    # ENV
    database_url: str
    debug: bool
    secret_key: str
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore


settings = get_settings()
