from pathlib import Path
import torch

# =====================================================
# PROJECT PATH
# =====================================================

# app/
BASE_DIR = Path(__file__).resolve().parent

# Project/
PROJECT_DIR = BASE_DIR.parent

# =====================================================
# DIRECTORIES
# =====================================================

# Upload
UPLOAD_DIR = PROJECT_DIR / "uploads"

# Output
OUTPUT_DIR = PROJECT_DIR / "output"

CARD_DIR = OUTPUT_DIR / "card"

FACE_DIR = OUTPUT_DIR / "face"

FIELD_DIR = OUTPUT_DIR / "fields"

JSON_DIR = OUTPUT_DIR / "json"

EXCEL_DIR = OUTPUT_DIR / "excel"

# Static & Template
STATIC_DIR = BASE_DIR / "static"

TEMPLATE_DIR = BASE_DIR / "templates"

# Model
MODEL_DIR = BASE_DIR / "models"

# =====================================================
# MODEL FILE
# =====================================================

CARD_SEG_MODEL = MODEL_DIR / "card_seg.pt"

FIELD_MODEL = MODEL_DIR / "field_detector.pt"

OCR_MODEL = MODEL_DIR / "vgg_transformer.pth"

# =====================================================
# DEVICE
# =====================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =====================================================
# YOLO CONFIG
# =====================================================

SEG_CONF = 0.50

FIELD_CONF = 0.40

PADDING = 5

# =====================================================
# FASTAPI
# =====================================================

API_TITLE = "OCR CCCD API"

API_VERSION = "1.0.0"

API_DESCRIPTION = "Vietnam Citizen ID OCR using YOLO11 + VietOCR"

API_HOST = "0.0.0.0"

API_PORT = 8000

API_RELOAD = True

# =====================================================
# IMAGE
# =====================================================

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20 MB

# =====================================================
# CREATE FOLDER
# =====================================================

for folder in [
    UPLOAD_DIR,
    OUTPUT_DIR,
    CARD_DIR,
    FACE_DIR,
    FIELD_DIR,
    JSON_DIR,
    EXCEL_DIR,
    STATIC_DIR,
    TEMPLATE_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

# =====================================================
# STATIC FILE
# =====================================================

NO_IMAGE = STATIC_DIR / "images" / "no-image.png"

NO_FACE = STATIC_DIR / "images" / "no-face.png"