from pydantic_settings import BaseSettings

from src.core.enum import Environment


class Settings(BaseSettings):
    # 환경 (ex: 상용환경, 개발환경)
    ENV: Environment = Environment.PROD
    # DB 설정
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str


settings = Settings()
