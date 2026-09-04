import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Load .env file
load_dotenv(PROJECT_ROOT / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "heritageverse-super-secret-key-2026-royal-india")
    
    # Upload Settings
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))  # 5 MB limit
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    
    # Database Settings
    # Supports MySQL URL or transparent fallback to SQLite if MySQL is offline
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "heritageverse")
    
    # Primary MySQL Connection URI
    _mysql_uri = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    
    # Allow explicit override from DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", _mysql_uri)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True
    }
    
    # Static Assets Directories
    FRONTEND_DIR = os.getenv("FRONTEND_DIR", str(PROJECT_ROOT / "frontend"))
