from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv(".env")


class Settings(BaseSettings):
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME: int = 1
    DATABASE_URL: str
    ADMIN_API_TOKEN: SecretStr

    class Config:
        env_file = ".env"
