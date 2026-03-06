"""Configuration centralisée de l'application."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Paramètres chargés depuis les variables d'environnement."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Base de données (SQLite par défaut)
    database_url: str = "sqlite+aiosqlite:///./dev_assist.db"

    # Chemins
    base_dir: Path = Path(__file__).resolve().parent.parent.parent


settings = Settings()
