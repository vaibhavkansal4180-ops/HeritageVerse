import os
import sys
from pathlib import Path
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from sqlalchemy import text

# Add project root to sys.path so package imports work reliably
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import Config
from backend.models import db
from backend.routes import (
    auth_bp, states_bp, heritage_bp, reports_bp,
    admin_bp, stats_bp, preservation_bp, alerts_bp
)
from backend.utils.response import error_response

def create_app(config_class=Config):
    app = Flask(__name__, static_folder=str(PROJECT_ROOT / "frontend"), static_url_path="")
    app.config.from_object(config_class)

    # Configure CORS dynamically based on environment configuration
    cors_origins = app.config.get("CORS_ORIGINS", "*")
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    # Safely create upload directory if filesystem is writable
    try:
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        os.makedirs(str(PROJECT_ROOT / "frontend" / "assets" / "images"), exist_ok=True)
    except Exception:
        pass  # Graceful fallback on read-only serverless runtimes

    # Initialize Database
    init_db(app)

    # Register API Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(states_bp)
    app.register_blueprint(heritage_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(preservation_bp)
    app.register_blueprint(alerts_bp)

    # Static Uploads Route
    @app.route("/api/uploads/<path:filename>")
    def serve_upload(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # Explicit HTML Page Routes (Supports clean URLs with and without .html)
    PAGE_MAPPINGS = {
        "": "index.html",
        "sites": "sites.html",
        "site-detail": "site-detail.html",
        "heritage": "sites.html",
        "heritage-detail": "site-detail.html",
        "report": "report.html",
        "track": "track.html",
        "my-reports": "my-reports.html",
        "encroachment": "encroachment.html",
        "alerts": "alerts.html",
        "dashboard": "admin.html",
        "admin": "admin.html",
        "login": "login.html",
        "register": "register.html"
    }

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    for route_name, target_file in PAGE_MAPPINGS.items():
        if route_name:
            def make_view(f=target_file):
                return lambda: send_from_directory(app.static_folder, f)
            app.add_url_rule(f"/{route_name}", endpoint=f"page_{route_name}", view_func=make_view(target_file))
            app.add_url_rule(f"/{route_name}.html", endpoint=f"page_html_{route_name}", view_func=make_view(target_file))

    @app.route("/<path:path>")
    def serve_frontend_pages(path):
        if path.startswith("api/"):
            return error_response("API endpoint not found", status_code=404)
        html_file = f"{path}.html"
        if (Path(app.static_folder) / html_file).exists():
            return send_from_directory(app.static_folder, html_file)
        if (Path(app.static_folder) / path).exists():
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    # Global Error Handlers (JSON for API, HTML for frontend)
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return error_response("File too large. Maximum allowed file size is 5MB.", status_code=413)

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return error_response("API endpoint not found", status_code=404)
        return send_from_directory(app.static_folder, "index.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return error_response("Internal server error. Please try again later.", status_code=500)

    return app


def init_db(app):
    """Initializes SQLAlchemy database connection and creates tables if they don't exist."""
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"[DB Warning] Could not auto-create tables on init: {e}")


# Default WSGI application instance
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    print("=" * 60)
    print(f" HERITAGEVERSE PRESERVATION PLATFORM RUNNING AT PORT {port}")
    print(f" Debug Mode: {debug_mode}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

