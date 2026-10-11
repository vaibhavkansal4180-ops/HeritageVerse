import sys
import traceback
from pathlib import Path

# Add project root to sys.path for Vercel serverless runtime
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from backend.app import create_app
    app = create_app()
    handler = app
except Exception as e:
    init_traceback = traceback.format_exc()
    print(f"[FATAL SERVERLESS STARTUP] {init_traceback}", file=sys.stderr)

    def app(environ, start_response):
        error_msg = (
            f"HERITAGEVERSE 2.0 INITIALIZATION ERROR\n"
            f"----------------------------------------\n"
            f"Exception: {type(e).__name__}: {str(e)}\n\n"
            f"Traceback:\n{init_traceback}\n"
        ).encode("utf-8")
        status = "500 Internal Server Error"
        response_headers = [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(error_msg)))
        ]
        start_response(status, response_headers)
        return [error_msg]

    handler = app
