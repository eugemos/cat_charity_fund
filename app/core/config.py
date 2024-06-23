from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_author: str = 'Москалянов Евгений'
    app_title: str = 'API QRKot'
    description: str = 'Сервис пожертвований для благотворительного фонда'
    secret: str = 'TOPSECRETs'
    first_superuser_email: Optional[EmailStr] = 'admin@admin.com'
    first_superuser_password: Optional[str] = 'ZZaaqq11'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    class Config:
        env_file = '.env'


settings = Settings()
