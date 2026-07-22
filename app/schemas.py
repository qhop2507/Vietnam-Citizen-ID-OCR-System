from typing import Optional

from pydantic import BaseModel, Field


# ===========================
# Health
# ===========================

class HealthResponse(BaseModel):
    status: str = "ok"


# ===========================
# OCR Result
# ===========================

class OCRData(BaseModel):

    id: Optional[str] = Field(
        default="",
        description="Citizen ID Number"
    )

    name: Optional[str] = Field(
        default="",
        description="Full Name"
    )

    dob: Optional[str] = Field(
        default="",
        description="Date of Birth"
    )

    gender: Optional[str] = Field(
        default="",
        description="Gender"
    )

    nationality: Optional[str] = Field(
        default="",
        description="Nationality"
    )

    origin_place: Optional[str] = Field(
        default="",
        description="Place of Origin"
    )

    current_place: Optional[str] = Field(
        default="",
        description="Current Residence"
    )

    expire_date: Optional[str] = Field(
        default="",
        description="Expiration Date"
    )

    issue_date: Optional[str] = Field(
        default="",
        description="Issue Date"
    )

    qr: Optional[str] = Field(
        default="",
        description="QR Code Content"
    )


# ===========================
# OCR Response
# ===========================

class OCRResponse(BaseModel):

    success: bool

    data: OCRData


# ===========================
# Error Response
# ===========================

class ErrorResponse(BaseModel):

    success: bool = False

    detail: str


# ===========================
# API Info
# ===========================

class RootResponse(BaseModel):

    message: str

    version: str

    swagger: str