# from pydantic_settings import BaseSettings
# import os

# class Settings(BaseSettings):
#     redis_url: str = "redis://localhost:6379/0"
#     default_cache_ttl: int = 10
#     poll_interval: float = 2.0
#     exchanges: list = ["binance", "kraken"]
#     cmc_api_key: str | None = None

#     class Config:
#         env_file = ".env"

# settings = Settings()


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    default_cache_ttl: int = 10
    poll_interval: float = 2.0
    exchanges: list[str] = ["binance", "kraken"]
    cmc_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env")

# ⭐ FIX: You MUST include this:
settings = Settings()
