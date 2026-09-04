import re
from flask import Blueprint, request
from backend.models import db, User
from backend.services.auth_service import generate_auth_token, token_required, get_current_user
from backend.utils.response import api_response, error_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or len(name) < 2:
        return error_response("Full name is required (minimum 2 characters).")
    
    if not email or not re.match(EMAIL_REGEX, email):
        return error_response("A valid email address is required.")
        
    if not password or len(password) < 6:
        return error_response("Password must be at least 6 characters long.")

    # Check existing user
    if User.query.filter_by(email=email).first():
        return error_response("An account with this email already exists. Please log in.", status_code=409)

    user = User(
        name=name,
        email=email,
        role="user"
    )
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error during registration: {str(e)}", status_code=500)

    token = generate_auth_token(user.id, user.role)
    return api_response(
        data={
            "user": user.to_dict(),
            "token": token
        },
        message="Registration successful! Welcome to HeritageVerse.",
        status_code=201
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return error_response("Email and password are required.")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return error_response("Invalid email or password. Please try again.", status_code=401)

    token = generate_auth_token(user.id, user.role)
    return api_response(
        data={
            "user": user.to_dict(),
            "token": token
        },
        message=f"Welcome back, {user.name}!"
    )


@auth_bp.route("/me", methods=["GET"])
@token_required
def get_me(current_user):
    return api_response(
        data={
            "user": current_user.to_dict()
        },
        message="User profile retrieved."
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return api_response(message="Logged out successfully.")
