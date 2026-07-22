from pathlib import Path
from typing import Dict, List, Union

import cv2
import numpy as np
import torch
from PIL import Image
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor


class VietOCRService:
    """
    OCR sử dụng VietOCR.
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        device: str = "cuda"
    ):

        model_path = Path(model_path)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy model: {model_path}"
            )

        if device == "cuda" and not torch.cuda.is_available():
            device = "cpu"

        config = Cfg.load_config_from_name("vgg_transformer")

        config["weights"] = str(model_path)
        config["device"] = device
        config["cnn"]["pretrained"] = False
        config["predictor"]["beamsearch"] = False

        self.predictor = Predictor(config)

    def predict_image(
        self,
        image: Union[np.ndarray, Image.Image]
    ) -> str:
        """
        OCR một ảnh.
        """

        if image is None:
            return ""

        try:

            if isinstance(image, np.ndarray):

                # OpenCV BGR -> RGB
                image = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2RGB
                )

                image = Image.fromarray(image)

            elif not isinstance(image, Image.Image):

                return ""

            text = self.predictor.predict(image)

            if text is None:
                return ""

            return str(text).strip()

        except Exception:
            return ""

    def predict_fields(
        self,
        fields: Dict[str, List[np.ndarray]]
    ) -> Dict[str, str]:
        """
        OCR toàn bộ các trường.
        """

        result: Dict[str, str] = {}

        for field_name, images in fields.items():

            if field_name.lower() == "qr":
                continue

            texts = []

            for image in images:

                text = self.predict_image(image)

                if text:
                    texts.append(text)

            result[field_name] = " ".join(texts).strip()

        return result