from pathlib import Path
from typing import Dict, Union

import cv2
import numpy as np
from ultralytics import YOLO


class CardSegmentation:
    """
    Phát hiện vùng CCCD bằng YOLO Segmentation.

    Trả về:
    {
        "image": image_goc,
        "polygon": polygon_4+_dinh
    }
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        conf: float = 0.5
    ):
        self.model = YOLO(str(model_path))
        self.conf = conf

    def segment(
        self,
        image: Union[str, Path, np.ndarray]
    ) -> Dict:

        # -------------------------
        # Load image
        # -------------------------
        if isinstance(image, (str, Path)):
            image = cv2.imread(str(image))

        if image is None:
            raise ValueError("Cannot read input image.")

        # -------------------------
        # Predict
        # -------------------------
        result = self.model.predict(
            source=image,
            conf=self.conf,
            verbose=False
        )[0]

        # -------------------------
        # Check result
        # -------------------------
        if result.masks is None:
            raise RuntimeError("Card not detected.")

        if len(result.masks.xy) == 0:
            raise RuntimeError("Segmentation mask is empty.")

        # -------------------------
        # Lấy mask có confidence cao nhất
        # -------------------------
        best_index = int(result.boxes.conf.argmax().item())

        polygon = result.masks.xy[best_index].astype(np.float32)

        return {
            "image": image,
            "polygon": polygon
        }

    def crop(
        self,
        image: np.ndarray,
        polygon: np.ndarray
    ) -> np.ndarray:
        """
        Crop nhanh theo BoundingRect.
        Chỉ dùng để debug hoặc xem kết quả.
        """

        polygon = polygon.astype(np.int32)

        mask = np.zeros(image.shape[:2], dtype=np.uint8)

        cv2.fillPoly(mask, [polygon], 255)

        segmented = cv2.bitwise_and(
            image,
            image,
            mask=mask
        )

        x, y, w, h = cv2.boundingRect(polygon)

        return segmented[y:y+h, x:x+w]

    def save(
        self,
        image: np.ndarray,
        output_path: Union[str, Path]
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        cv2.imwrite(
            str(output_path),
            image,
            [cv2.IMWRITE_JPEG_QUALITY, 100]
        )