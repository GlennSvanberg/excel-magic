# config.py

import os

class Config:
    # Base directory for saving uploaded files
    UPLOAD_FOLDER = 'static/uploads'
    # Allowed file extensions for upload
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    # Maximum file size that can be uploaded (in bytes)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

