import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Load .env file if present
load_dotenv(PROJECT_ROOT / ".env")

class Config:
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY") or "heritageverse-super-secret-key-2026-royal-india"
    FLASK_ENV = os.getenv("FLASK_ENV") or "development"
    DEBUG = (os.getenv("DEBUG") or "false").lower() in ("true", "1", "yes")

    # Environment detection: Identifies Vercel serverless or production hosting
    IS_VERCEL = (os.getenv("VERCEL") or "") == "1"
    IS_PRODUCTION = (
        FLASK_ENV.lower() == "production"
        or IS_VERCEL
        or (os.getenv("ENV") or "").lower() == "production"
        or (os.getenv("NODE_ENV") or "").lower() == "production"
    )

    # Upload Settings (Gracefully handles read-only serverless filesystems and empty env vars)
    _default_upload = str(BASE_DIR / "uploads")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER") or _default_upload
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH") or 5 * 1024 * 1024)  # 5 MB limit
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Database Settings
    # Supports PostgreSQL via DATABASE_URL (Neon, Supabase, Vercel Postgres, AWS RDS, etc.)
    # Automatically converts legacy 'postgres://' to 'postgresql://' for SQLAlchemy compatibility
    _raw_db_url = os.getenv("DATABASE_URL")
    if _raw_db_url and _raw_db_url.strip():
        _clean_url = _raw_db_url.strip()
        if _clean_url.startswith("postgres://"):
            _clean_url = _clean_url.replace("postgres://", "postgresql://", 1)
        if IS_PRODUCTION and _clean_url.startswith("sqlite"):
            raise RuntimeError(
                "FATAL CONFIGURATION ERROR: SQLite database URI is not supported in a production/Vercel environment. "
                "Please configure a valid PostgreSQL DATABASE_URL in your environment variables."
            )
        SQLALCHEMY_DATABASE_URI = _clean_url
    else:
        # In production/Vercel, fail loudly with a clear configuration error if DATABASE_URL is missing
        if IS_PRODUCTION:
            raise RuntimeError(
                "FATAL CONFIGURATION ERROR: DATABASE_URL environment variable is missing in production/Vercel environment. "
                "A managed PostgreSQL database connection string is required (e.g. from Neon, Supabase, Vercel Postgres, AWS RDS). "
                "Format: postgresql://<user>:<password>@<host>:5432/<dbname>?sslmode=require"
            )
        # Transparent fallback to local SQLite ONLY for local development/testing
        _sqlite_path = BASE_DIR / "heritageverse.db"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{_sqlite_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    # CORS Settings
    _cors_raw = os.getenv("CORS_ORIGINS") or "*"
    CORS_ORIGINS = [o.strip() for o in _cors_raw.split(",")] if "," in _cors_raw else _cors_raw

    # Static Assets Directory
    FRONTEND_DIR = os.getenv("FRONTEND_DIR") or str(PROJECT_ROOT / "frontend")
