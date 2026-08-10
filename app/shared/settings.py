from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str 
    environment: str 
    database_url: str 
    
    jwt_secret_key: str
    jwt_expiracao_minutos: int 

    seed_admin_email: str 
    seed_admin_senha: str


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
