from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    APP_NAME: str = "FIXTLE"
    SECRET_KEY: str = "turtlelite-super-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 horas (jornada laboral)
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ventas.db")
    
    # Horario informativo
    HORARIO_INICIO: str = "08:00"
    HORARIO_FIN: str = "18:00"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
