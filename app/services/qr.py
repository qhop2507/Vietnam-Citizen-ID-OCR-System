from pathlib import Path
from typing import Dict, List, Union

import cv2
import numpy as np


class QRService:
    """
    Dịch vụ đọc mã QR sử dụng OpenCV QRCodeDetector.
    """

    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def decode_image(
        self,
        image: np.ndarray
    ) -> str:
        """
        Đọc QR từ ảnh.

        Parameters
        ----------
        image : np.ndarray

        Returns
        -------
        str
            Nội dung QR hoặc chuỗi rỗng nếu không đọc được.
        """

        if image is None:
            return ""

        if image.size == 0:
            return ""

        try:

            # Thử ảnh gốc
            text, _, _ = self.detector.detectAndDecode(image)

            if text:
                return text.strip()

            # Nếu chưa được thì thử grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2GRAY
                )

                text, _, _ = self.detector.detectAndDecode(gray)

                if text:
                    return text.strip()

            return ""

        except Exception:
            return ""

    def decode_file(
        self,
        image_path: Union[str, Path]
    ) -> str:
        """
        Đọc QR từ file ảnh.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            return ""

        image = cv2.imread(str(image_path))

        if image is None:
            return ""

        return self.decode_image(image)

    def decode_fields(
        self,
        fields: Dict[str, List[np.ndarray]]
    ) -> str:
        """
        Đọc QR từ kết quả Field Detector.

        Parameters
        ----------
        fields : dict

            {
                "qr": [img1]
            }

        Returns
        -------
        str
            Nội dung QR.
        """

        images = fields.get("qr")

        if not images:
            return ""

        for image in images:

            text = self.decode_image(image)

            if text:
                return text

        return ""