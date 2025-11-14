"""
Configuration management using Pydantic Settings.
Loads environment variables from .env file.
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Firebase configuration
    firebase_credentials_path: str = "firebase_account_services.json"
    
    # Frontend configuration
    frontend_url: str = "http://localhost:5173"
    
    # Admin emails (hardcoded for now, move to database later)
    # Can be set as comma-separated string in .env: ADMIN_EMAILS=admin@photolog.com,admin2@photolog.com
    admin_emails: str = "admin@photolog.com"
    
    def get_admin_emails_list(self) -> list[str]:
        """Get admin emails as a list."""
        if not self.admin_emails:
            return []
        return [email.strip() for email in self.admin_emails.split(",") if email.strip()]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_firebase_credentials_path() -> Path:
    """Get the path to Firebase credentials file."""
    cred_path = Path(settings.firebase_credentials_path)
    if not cred_path.is_absolute():
        # Since the server is always run from the backend directory,
        # use the current working directory as the base path
        backend_dir = Path(os.getcwd())
        cred_path = backend_dir / cred_path
    return cred_path.resolve()

