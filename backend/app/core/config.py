# app/core/config.py
from __future__ import annotations

from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError


class Settings(BaseSettings):
    # === Database (MySQL) ===
    # Am înlocuit SQLSERVER_CONN_STR cu variabile individuale pentru MySQL
    MYSQL_USER: str = Field("root", description="Utilizatorul MySQL")
    MYSQL_PASSWORD: str = Field(..., description="Parola MySQL")
    MYSQL_HOST: str = Field("localhost", description="Host-ul serverului MySQL")
    MYSQL_PORT: str = Field("3306", description="Portul MySQL (default 3306)")
    MYSQL_DB: str = Field("Smart_librarian_users", description="Numele bazei de date")

    # === Providers / APIs ===
    GROQ_API_KEY: str = Field(..., description="OpenAI API key")

    # === Auth / JWT ===
    JWT_SECRET: str = Field(..., description="JWT secret")
    JWT_ALG: str = Field("HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24, description="JWT expiry minutes")

    # === RAG / ChromaDB ===
    CHROMA_DIR: str = Field("./chroma_store", description="ChromaDB persistence directory")
    COLLECTION_NAME: str = Field("books", description="Default Chroma collection name")

    # === Models (names kept in env for flexibility) ===
    EMBED_MODEL: str = Field("text-embedding-3-small", description="Embedding model name")
    CHAT_MODEL: str = Field("gpt-4o-mini", description="Chat model name")

    # === CORS ===
    CORS_ORIGINS: str = Field(
        "http://localhost:3000,http://127.0.0.1:3000",
        description="Comma-separated list of allowed origins",
    )

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # ignore unknown env vars instead of failing hard

    @property
    def database_url(self) -> str:
        """
        Construiește URL-ul de conexiune pentru MySQL folosind driver-ul pymysql.
        Se folosește quote_plus pentru parolă pentru a evita erorile cauzate de caractere speciale.
        """
        user = self.MYSQL_USER
        password = quote_plus(self.MYSQL_PASSWORD)
        host = self.MYSQL_HOST
        port = self.MYSQL_PORT
        db = self.MYSQL_DB
        
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"


@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        missing = ", ".join(err.get("loc")[0] for err in e.errors() if err.get("type") == "missing")
        extras = ", ".join(err.get("loc")[0] for err in e.errors() if "extra_forbidden" in err.get("type", ""))
        parts = []
        if missing:
            parts.append(f"Missing required environment variables: {missing}")
        if extras:
            parts.append(f"Unknown environment variables (ignored or add fields): {extras}")
        raise RuntimeError(" | ".join(parts) or str(e))