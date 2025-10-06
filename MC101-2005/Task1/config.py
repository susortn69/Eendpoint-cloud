from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv(".env")  # take environment variables from .env file


class Settings(BaseSettings):
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME: int = 3600

    class Config:
        env_file = ".env"


