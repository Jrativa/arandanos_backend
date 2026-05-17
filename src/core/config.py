# src/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_ENGINE: str = "postgres"  # Cambia esto a "mongo" cuando quieras probar
    
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_ENGINE == "postgres":
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_ENGINE == "mongo":
            return f"mongodb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            raise ValueError(f"Motor no soportado: {self.DB_ENGINE}")

    class Config:
        env_file = ".env"

settings = Settings()