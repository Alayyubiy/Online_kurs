import os
import uuid
import shutil
import magic  # pip install python-magic
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads/courses"

# ✅ FIX 1: Ruxsat berilgan fayl turlari
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_IMAGE_MIMES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
ALLOWED_VIDEO_MIMES = {"video/mp4", "video/avi", "video/quicktime", "video/x-matroska", "video/webm"}

ALLOWED_DOC_EXTENSIONS = {".pdf", ".docx", ".doc"}
ALLOWED_DOC_MIMES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword"
}

# ✅ FIX 2: Fayl hajmi cheklovlari
MAX_IMAGE_SIZE = 5 * 1024 * 1024    # 5 MB
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB
MAX_DOC_SIZE = 20 * 1024 * 1024     # 20 MB


def _get_file_extension(filename: str) -> str:
    """Fayl kengaytmasini xavfsiz olish"""
    if not filename or "." not in filename:
        return ""
    return os.path.splitext(filename)[1].lower()


def _validate_file_content(file_path: str, allowed_mimes: set) -> bool:
    """Fayl mazmunini MIME type orqali tekshirish (kengaytmaga ishonmaslik!)"""
    try:
        mime = magic.from_file(file_path, mime=True)
        return mime in allowed_mimes
    except Exception:
        return False


def _check_file_size(file: UploadFile, max_size: int):
    """Fayl hajmini tekshirish"""
    file.file.seek(0, 2)  # Faylning oxiriga o'tish
    size = file.file.tell()
    file.file.seek(0)     # Boshiga qaytish

    if size > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"Fayl hajmi {max_size // (1024*1024)} MB dan oshmasligi kerak"
        )


def _save_with_unique_name(file: UploadFile, upload_dir: str) -> str:
    """
    ✅ FIX 3: Original fayl nomini ishlatmaslik!
    UUID bilan noyob nom yaratish - path traversal hujumini oldini oladi.
    """
    os.makedirs(upload_dir, exist_ok=True)

    ext = _get_file_extension(file.filename or "")
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def save_image(image: UploadFile) -> str:
    """Rasm saqlash - validatsiya bilan"""
    # ✅ Kengaytmani tekshirish
    ext = _get_file_extension(image.filename or "")
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Rasm uchun faqat {', '.join(ALLOWED_IMAGE_EXTENSIONS)} turlari ruxsat etilgan"
        )

    # ✅ Hajmini tekshirish
    _check_file_size(image, MAX_IMAGE_SIZE)

    # ✅ Faylni saqlash (noyob nom bilan)
    file_path = _save_with_unique_name(image, f"{UPLOAD_DIR}/images")

    # ✅ MIME type orqali haqiqiy tarkibni tekshirish
    if not _validate_file_content(file_path, ALLOWED_IMAGE_MIMES):
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Rasm fayli yaroqsiz yoki zararli")

    return file_path


def save_video(video: UploadFile) -> str:
    """Video saqlash - validatsiya bilan"""
    ext = _get_file_extension(video.filename or "")
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Video uchun faqat {', '.join(ALLOWED_VIDEO_EXTENSIONS)} turlari ruxsat etilgan"
        )

    _check_file_size(video, MAX_VIDEO_SIZE)
    file_path = _save_with_unique_name(video, f"{UPLOAD_DIR}/videos")

    if not _validate_file_content(file_path, ALLOWED_VIDEO_MIMES):
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Video fayli yaroqsiz yoki zararli")

    return file_path


def save_document(doc: UploadFile) -> str:
    """Hujjat saqlash (PDF, DOCX) - validatsiya bilan"""
    ext = _get_file_extension(doc.filename or "")
    if ext not in ALLOWED_DOC_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Hujjat uchun faqat {', '.join(ALLOWED_DOC_EXTENSIONS)} turlari ruxsat etilgan"
        )

    _check_file_size(doc, MAX_DOC_SIZE)
    file_path = _save_with_unique_name(doc, f"{UPLOAD_DIR}/docs")

    if not _validate_file_content(file_path, ALLOWED_DOC_MIMES):
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Hujjat fayli yaroqsiz yoki zararli")

    return file_path


# Orqaga muvofiqlik uchun
save_file = save_document