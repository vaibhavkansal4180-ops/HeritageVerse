import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from backend.config import Config

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/pjpeg'}

def allowed_file(filename: str) -> bool:
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def validate_and_save_image(file_storage, upload_folder: str = None) -> dict:
    """
    Validates an uploaded image file securely and saves it to the uploads directory.
    Returns metadata dictionary or raises ValueError.
    """
    if not file_storage or file_storage.filename == '':
        raise ValueError("No file selected for upload.")

    # 1. Filename validation
    original_filename = secure_filename(file_storage.filename)
    if not allowed_file(original_filename):
        raise ValueError(f"Invalid file extension. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}")

    # 2. MIME type check
    content_type = file_storage.content_type
    if content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Invalid image type ({content_type}). Please upload a valid JPEG, PNG, or WEBP image.")

    # 3. Read stream to check size
    file_bytes = file_storage.read()
    file_size = len(file_bytes)
    
    if file_size > Config.MAX_CONTENT_LENGTH:
        raise ValueError(f"File exceeds maximum allowed size of {Config.MAX_CONTENT_LENGTH // (1024 * 1024)}MB.")
    
    if file_size == 0:
        raise ValueError("Uploaded file is empty.")

    # 4. Check file magic bytes for common image headers
    is_valid_header = False
    if file_bytes.startswith(b'\xff\xd8\xff'): # JPEG
        is_valid_header = True
    elif file_bytes.startswith(b'\x89PNG\r\n\x1a\n'): # PNG
        is_valid_header = True
    elif file_bytes.startswith(b'RIFF') and b'WEBP' in file_bytes[:16]: # WEBP
        is_valid_header = True

    if not is_valid_header:
        raise ValueError("File content does not match a valid image format.")

    # 5. Generate secure random filename
    ext = original_filename.rsplit('.', 1)[1].lower()
    safe_filename = f"evidence_{uuid.uuid4().hex}.{ext}"

    # Target folder
    dest_dir = Path(upload_folder or Config.UPLOAD_FOLDER)
    dest_dir.mkdir(parents=True, exist_ok=True)

    file_path = dest_dir / safe_filename

    # 6. Save file safely
    with open(file_path, 'wb') as f:
        f.write(file_bytes)

    # 7. Return safe web-accessible relative URL & metadata
    return {
        "saved_filename": safe_filename,
        "original_filename": original_filename,
        "image_url": f"/api/uploads/{safe_filename}",
        "url": f"/api/uploads/{safe_filename}",
        "file_size": file_size,
        "file_size_bytes": file_size,
        "mime_type": content_type
    }

def save_uploaded_image(file_storage, upload_folder: str = None) -> dict:
    """Wrapper around validate_and_save_image."""
    return validate_and_save_image(file_storage, upload_folder)

