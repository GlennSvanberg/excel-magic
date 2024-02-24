# config.py

import os

class Config:
    # Base directory for saving uploaded files
    UPLOAD_FOLDER = 'static/uploads'

    PLAYGROUND_FOLDER = 'playground'

    OUTPUT_FOLDER = 'static/output'
    # Allowed file extensions for upload
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    # Maximum file size that can be uploaded (in bytes)
    MAX_CONTENT_LENGTH = 128 * 1024 * 1024  # 128 MB

    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(PLAYGROUND_FOLDER):
        os.makedirs(PLAYGROUND_FOLDER)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
