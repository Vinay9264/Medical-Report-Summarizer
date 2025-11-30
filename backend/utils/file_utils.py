import os
from fastapi import UploadFile
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

async def save_file(file: UploadFile) -> str:
    """
    Saves uploaded file (PDF or Image) into /uploads directory.
    Returns the saved file path.
    """
    file_ext = file.filename.split(".")[-1].lower()
    file_path = UPLOAD_DIR / file.filename

    
    file_bytes = await file.read()

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return str(file_path)
