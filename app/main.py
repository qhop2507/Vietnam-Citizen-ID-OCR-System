import shutil
from pathlib import Path

import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import *
from app.services.segmentation import CardSegmentation
from app.services.perspective import PerspectiveTransform
from app.services.field_detector import FieldDetector
from app.services.ocr import VietOCRService
from app.services.qr import QRService
from app.services.postprocess import PostProcessor

# ======================================================
# FastAPI
# ======================================================

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# ======================================================
# Static
# ======================================================

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

app.mount(
    "/output",
    StaticFiles(directory=OUTPUT_DIR),
    name="output"
)

templates = Jinja2Templates(directory=TEMPLATE_DIR)

# ======================================================
# Load model (chỉ load 1 lần)
# ======================================================

segmentor = CardSegmentation(
    model_path=CARD_SEG_MODEL,
    conf=SEG_CONF
)

field_detector = FieldDetector(
    model_path=FIELD_MODEL,
    conf=FIELD_CONF
)

ocr = VietOCRService(
    model_path=OCR_MODEL,
    device=DEVICE
)

qr = QRService()

post = PostProcessor()

# ======================================================
# Home
# ======================================================

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# ======================================================
# Health
# ======================================================

@app.get("/health")
def health():
    return {"status": "ok"}

# ======================================================
# OCR
# ======================================================

@app.post("/ocr")
async def detect_cccd(
    image: UploadFile = File(...)
):

    suffix = Path(image.filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Định dạng ảnh không được hỗ trợ."
        )

    image_path = UPLOAD_DIR / image.filename

    try:

        # ---------------------------------
        # Save upload
        # ---------------------------------

        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        # ---------------------------------
        # Segmentation
        # ---------------------------------

        seg_result = segmentor.segment(image_path)

        card = PerspectiveTransform.transform(
            seg_result["image"],
            seg_result["polygon"]
        )

        card_path = CARD_DIR / f"{image_path.stem}.jpg"

        cv2.imwrite(
            str(card_path),
            card,
            [cv2.IMWRITE_JPEG_QUALITY, 100]
        )

        # ---------------------------------
        # Field Detection
        # ---------------------------------

        fields = field_detector.detect(card)

        field_detector.save(
            fields,
            FIELD_DIR
        )

        # ---------------------------------
        # Save Face
        # ---------------------------------

        face_path = None

        if "face" in fields and len(fields["face"]) > 0:

            face_path = FACE_DIR / f"{image_path.stem}.jpg"

            cv2.imwrite(
                str(face_path),
                fields["face"][0],
                [cv2.IMWRITE_JPEG_QUALITY, 100]
            )

        # ---------------------------------
        # OCR
        # ---------------------------------

        result = ocr.predict_fields(fields)

        # ---------------------------------
        # QR
        # ---------------------------------

        result["qr"] = qr.decode_fields(fields)

        # ---------------------------------
        # Post Process
        # ---------------------------------

        result = post.process(result)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "card_image": f"/output/card/{image_path.stem}.jpg",
                "face_image": (
                    f"/output/face/{image_path.stem}.jpg"
                    if face_path
                    else ""
                ),
                "data": result
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )