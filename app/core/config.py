from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # JWT
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    token_algorithm: str = 'HS256'

    # YOOKASSA
    yookassa_shop_id: str
    yookassa_secret_key: str
    yookassa_return_url: str

    # Subscription
    subscribtion_price: str = '1000.00'
    subscribtion_currency: str = 'RUB'
    subscribtion_desc: str = 'Подписка Pro'

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
