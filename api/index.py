import sys
from pathlib import Path

# Add project root to sys.path for Vercel serverless runtime
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import traceback
from flask import Flask, jsonify

try:
    from backend.app import create_app
    app = create_app()
except Exception as e:
    tb = traceback.format_exc()
    print(f"[Startup Fatal Error] {tb}")
    app = Flask(__name__)
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return jsonify({
            "error": "Serverless application startup error",
            "message": str(e),
            "traceback": tb
        }), 500
