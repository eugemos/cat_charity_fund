from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_author: str = 'Москалянов Евгений'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    app_title: str = 'API QRKot'
    description: str = 'Финальный проект по FastAPI'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'admin@admin.com'
    first_superuser_password: Optional[str] = 'ZZaaqq11'

    class Config:
        env_file = '.env'


settings = Settings()
