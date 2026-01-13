import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    MAX_COMPETITORS: int = int(os.getenv("MAX_COMPETITORS", "10"))
    DEFAULT_LOCATION: str = "Germany"
    DEFAULT_LANGUAGE: str = "German"

settings = Config()
