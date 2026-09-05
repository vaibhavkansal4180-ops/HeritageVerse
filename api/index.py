import sys
from pathlib import Path

# Add project root to sys.path for Vercel serverless runtime
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app import create_app

# Vercel serverless WSGI entrypoint
app = create_app()
