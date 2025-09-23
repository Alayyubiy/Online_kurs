import shutil
import os

from fastapi import UploadFile

UPLOAD_DIR = "uploads/courses"

def save_image(image: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, image.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return file_path
save_file = save_image
