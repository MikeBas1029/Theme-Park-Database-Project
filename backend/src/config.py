from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str 
    SSL_CERT: str
    JWT_SECRET: str 
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()