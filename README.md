<h1 align="center">
🇻🇳 Vietnam Citizen ID OCR System
</h1>

<p align="center">
<b>End-to-End AI-powered Vietnamese Citizen ID Card Recognition System</b>
</p>

<p align="center">
An intelligent OCR framework for Vietnamese Citizen Identification Cards (CCCD),
combining <b>YOLO11 Segmentation</b>, <b>Perspective Transformation</b>,
<b>YOLO11 Detection</b>, <b>VietOCR</b>, and <b>FastAPI</b> to automatically
detect, rectify, recognize, and extract structured information from ID cards.
</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white">

<img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?logo=pytorch&logoColor=white">

<img src="https://img.shields.io/badge/YOLO11-Ultralytics-8A2BE2">

<img src="https://img.shields.io/badge/VietOCR-OCR-orange">

<img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv&logoColor=white">

<img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white">

<img src="https://img.shields.io/badge/License-MIT-yellow">

</p>

---

## 📖 Overview

Vietnam Citizen ID OCR System is an end-to-end computer vision pipeline that automatically extracts information from Vietnamese Citizen Identification Cards (CCCD).

The system leverages modern deep learning techniques for document understanding, including card segmentation, geometric correction, information field detection, optical character recognition, QR code decoding, and structured data extraction.

---

## ✨ Features

- 🇻🇳 Vietnamese Citizen ID Card Recognition
- 📄 Automatic Card Detection
- ✂️ Card Segmentation
- 📐 Perspective Correction
- 🔍 Information Field Detection
- 🤖 OCR using VietOCR
- 🔳 QR Code Recognition
- 👤 Face Image Extraction
- 📦 JSON Output
- 🌐 FastAPI Web Application
- ⚡ High-speed Inference

---

## 🏗️ System Pipeline

```text
                Input Image
                     │
                     ▼
      YOLO11 Card Segmentation
                     │
                     ▼
      Perspective Transformation
                     │
                     ▼
      YOLO11 Field Detection
                     │
                     ▼
      Crop Information Fields
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   VietOCR                 QR Decoder
        │                         │
        └────────────┬────────────┘
                     ▼
             Post Processing
                     │
                     ▼
              Structured JSON
```

---

## 🛠️ Technologies

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Detection | YOLO11 |
| OCR | VietOCR |
| Image Processing | OpenCV |
| Deep Learning | PyTorch |
| Language | Python |
| Deployment | Uvicorn |

---

## 📂 Project Structure

```text
Vietnam-Citizen-ID-OCR-System
│
├── app
│   ├── models
│   ├── services
│   ├── static
│   ├── templates
│   ├── config.py
│   ├── main.py
│   └── schemas.py
│
├── uploads
├── output
├── requirements.txt
├── run.py
└── README.md
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/your_username/Vietnam-Citizen-ID-OCR-System.git

cd Vietnam-Citizen-ID-OCR-System
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## 📊 Supported Information

- Citizen ID Number
- Full Name
- Date of Birth
- Gender
- Nationality
- Place of Origin
- Current Residence
- Issue Date
- Expiry Date
- Face Image
- QR Code

---

## 📷 Demo

### Original Image

> *(Add your demo image here)*

↓

### Recognition Result

- Card Detection
- Perspective Correction
- OCR Result
- Face Extraction
- JSON Output

---

## 📈 Future Improvements

- Batch Processing
- PDF Support
- Docker Deployment
- ONNX/TensorRT Inference
- REST API Authentication
- Multi-language OCR
- Mobile Deployment

---

## ⭐ If you find this project useful

Give this repository a ⭐ on GitHub.
