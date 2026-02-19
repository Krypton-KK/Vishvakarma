import os
from typing import List

from pydantic_settings import BaseSettings
import dotenv

class Settings(BaseSettings):
    APP_DIR: str = os.path.dirname(os.path.abspath(__file__))
    env_file: str = f"{APP_DIR}/../.env"
    dotenv.load_dotenv(dotenv_path=env_file)
    APP_NAME: str = os.getenv("APP_NAME")
    MAX_RESULTS: int = int(os.getenv("MAX_RESULTS"))
    API_KEY: List[str] = os.getenv("API_KEY")

settings = Settings()
# print(settings.APP_DIR)
# print(settings.env_file)
# print(settings.APP_NAME)
# print(settings.MAX_RESULTS)
# print(settings.API_KEY)
# print(type(settings.API_KEY))
