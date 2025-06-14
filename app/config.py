import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

class Settings:

    #app config
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Project")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Auth settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # HF config
    HF_API_TOKEN: str = os.getenv("HF_API_TOKEN")
    HF_MODEL_ID: str = os.getenv("HF_MODEL_ID")

    # DB
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # EMAIL CONFIG – tout en str
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")  # PAS EmailStr
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT") or 587)
    MAIL_SERVER: str = os.getenv("MAIL_SERVER") or "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME") or "OmniMed"

settings = Settings()
