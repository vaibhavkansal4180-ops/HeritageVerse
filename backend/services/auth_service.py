from functools import wraps
from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from backend.models.user import User
from backend.utils.response import error_response

def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

def generate_auth_token(user_id: int, role: str, expires_in: int = 86400 * 7) -> str:
    """Generates a secure timed token for user session (valid for 7 days by default)."""
    s = get_serializer()
    return s.dumps({"user_id": user_id, "role": role})

def decode_auth_token(token: str, max_age: int = 86400 * 7) -> dict:
    """Decodes and validates a session token."""
    s = get_serializer()
    try:
        data = s.loads(token, max_age=max_age)
        return data
    except (SignatureExpired, BadTimeSignature):
        return None
    except Exception:
        return None

def get_current_user():
    """Extracts and verifies user from Authorization header or session token."""
    auth_header = request.headers.get("Authorization")
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    elif request.cookies.get("token"):
        token = request.cookies.get("token")
    
    if not token:
        return None

    data = decode_auth_token(token)
    if not data:
        return None

    user = User.query.get(data.get("user_id"))
    return user

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return error_response("Authentication required. Please log in.", status_code=401)
        return f(user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return error_response("Authentication required.", status_code=401)
        if user.role != "admin":
            return error_response("Forbidden: Admin access required.", status_code=403)
        return f(user, *args, **kwargs)
    return decorated
