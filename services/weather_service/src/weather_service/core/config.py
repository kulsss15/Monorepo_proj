from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather Decision Service"
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    OPENWEATHER_API_KEY: str = Field(..., env="OPENWEATHER_API_KEY")
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()