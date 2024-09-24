from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class RunConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8080

class ApiPrefix(BaseModel):
    prefix: str = '/api'

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    db_url: str = os.getenv("DB")

settings = Settings()