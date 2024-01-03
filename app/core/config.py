from typing import Optional
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_author: str
    database_url: str
    # path: str
    app_title: str = 'API QRKot'
    description: str = 'Финальный проект по FastAPI'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
