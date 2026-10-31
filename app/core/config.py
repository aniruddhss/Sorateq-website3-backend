import json
import os
from typing import List, Union, Optional
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sorateq_db"
    SYNC_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/sorateq_db"
    
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    SUPABASE_ANON_KEY: str = ""

    # AI Keys
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Model Selection
    GEMINI_MODEL: str = "gemini-2.0-flash-lite"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    ROUTING_FAST_MODEL: str = "gemini-2.0-flash-lite"
    ROUTING_PRIMARY_MODEL: str = "gemini-2.0-flash-lite"
    ROUTING_REASONING_MODEL: str = "gemini-2.5-pro"

    # Server / Render Port
    PORT: Optional[int] = None
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://sorateq.com",
        "https://www.sorateq.com",
        "*"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    @model_validator(mode="after")
    def assemble_settings(self):
        # 1. Align PORT for Render / Cloud (Render passes $PORT)
        env_port = os.environ.get("PORT")
        if env_port:
            try:
                self.BACKEND_PORT = int(env_port)
            except ValueError:
                pass
        elif self.PORT:
            self.BACKEND_PORT = self.PORT

        # 2. Normalize DATABASE_URL and SYNC_DATABASE_URL
        db_url = (self.DATABASE_URL or "").strip()
        
        # Replace legacy postgres:// with postgresql://
        if db_url.startswith("postgres://"):
            db_url = "postgresql://" + db_url[len("postgres://"):]

        # Create sync version if default or empty
        sync_url = (self.SYNC_DATABASE_URL or "").strip()
        if not sync_url or "localhost:5432/sorateq_db" in sync_url:
            if db_url.startswith("postgresql+asyncpg://"):
                sync_url = "postgresql://" + db_url[len("postgresql+asyncpg://"):]
            else:
                sync_url = db_url

        # Ensure async URL uses postgresql+asyncpg:// driver
        if not db_url.startswith("postgresql+asyncpg://"):
            if db_url.startswith("postgresql://"):
                db_url = "postgresql+asyncpg://" + db_url[len("postgresql://"):]

        # Strip sslmode from asyncpg query string (asyncpg raises if sslmode is in URL query)
        if "postgresql+asyncpg://" in db_url and "sslmode" in db_url:
            parsed = urlparse(db_url)
            qs = parse_qs(parsed.query)
            qs.pop("sslmode", None)
            new_query = urlencode(qs, doseq=True)
            db_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

        self.DATABASE_URL = db_url
        self.SYNC_DATABASE_URL = sync_url

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
