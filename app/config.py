from pydantic import BaseSettings, AnyHttpUrl
from typing import Optional

class Settings(BaseSettings):
    # app
    app_name: str = "RPi-NMS"
    env: str = "development"
    db_path: str = "data/rpi_nms.db"

    # network
    default_network: str = "192.168.1.0/24"
    scan_interval_minutes: int = 5

    # telegram
    telegram_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    # auth
    secret_key: str = "replace-me-with-secure-random"
    access_token_expire_minutes: int = 60

    # email (SMTP)
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_pass: Optional[str] = None
    smtp_from: Optional[str] = None

    # webhooks — list represented as comma-separated URLs in env, parsed by code
    webhook_urls: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
