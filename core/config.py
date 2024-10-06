import os

from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import BaseModel, PostgresDsn


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class JSONFilePath(BaseModel):
    base_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Путь к корневой папке проекта
    client: str = os.path.join(base_dir, 'client', 'config.json')
    server: str = os.path.join(base_dir, 'server', 'config.json')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    
    db: DatabaseConfig
    json_path: JSONFilePath = JSONFilePath()


settings = Settings()

