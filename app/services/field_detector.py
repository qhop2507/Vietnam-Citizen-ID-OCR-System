from pathlib import Path
from typing import Dict, List

import cv2
import numpy as np
from ultralytics import YOLO

from app.config import PADDING


class FieldDetector:
    """
    Phát hiện các trường thông tin trên CCCD.

    Kết quả trả về:
    {
        "id": [img1],
        "name": [img2],
        "current_place": [img3, img4],
        ...
    }
    """

    def __init__(
        self,
        model_path: str,
        conf: float = 0.4,
        padding: int = PADDING
    ):
        self.model = YOLO(str(model_path))
        self.conf = conf
        self.padding = padding

    def detect(self, image: np.ndarray) -> Dict[str, List[np.ndarray]]:
        """
        Parameters
        ----------
        image : np.ndarray
            Ảnh CCCD sau Perspective Transform.

        Returns
        -------
        dict
            Dictionary chứa các vùng crop theo từng nhãn.
        """

        if image is None:
            raise ValueError("Input image is None.")

        if image.size == 0:
            raise ValueError("Input image is empty.")

        result = self.model.predict(
            source=image,
            conf=self.conf,
            verbose=False
        )[0]

        fields: Dict[str, List[np.ndarray]] = {}

        h, w = image.shape[:2]

        # Sắp xếp theo vị trí đọc
        boxes = sorted(
            result.boxes,
            key=lambda b: (
                float(b.xyxy[0][1]),
                float(b.xyxy[0][0])
            )
        )

        for box in boxes:

            cls = int(box.cls.item())
            label = self.model.names[cls]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            x1 = max(0, x1 - self.padding)
            y1 = max(0, y1 - self.padding)

            x2 = min(w, x2 + self.padding)
            y2 = min(h, y2 + self.padding)

            crop = image[y1:y2, x1:x2]

            if crop is None or crop.size == 0:
                continue

            fields.setdefault(label, []).append(crop)

        return fields

    def save(
        self,
        fields: Dict[str, List[np.ndarray]],
        output_dir: Path
    ) -> None:
        """
        Lưu các ảnh crop ra thư mục.

        Parameters
        ----------
        fields : dict
            Dictionary trả về từ detect().
        output_dir : Path
            Thư mục lưu ảnh.
        """

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        for label, images in fields.items():

            for index, img in enumerate(images, start=1):

                if img is None:
                    continue

                if img.size == 0:
                    continue

                filename = output_dir / f"{label}_{index}.jpg"

                cv2.imwrite(
                    str(filename),
                    img,
                    [cv2.IMWRITE_JPEG_QUALITY, 100]
                )