from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class RunConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8080

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db_url: str = os.getenv("DB")

settings = Settings()