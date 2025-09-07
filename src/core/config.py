from pydantic_settings import BaseSettings

from src.core.enum import Environment


class Settings(BaseSettings):
    # 환경 (ex: 상용환경, 개발환경)
    ENV: Environment = Environment.PROD
    # Database
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int


settings = Settings()
