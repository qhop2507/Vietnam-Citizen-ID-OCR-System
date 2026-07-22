import cv2
import numpy as np


class PerspectiveTransform:
    """
    Thực hiện Perspective Transform từ polygon YOLO Segmentation.
    """

    @staticmethod
    def order_points(pts: np.ndarray) -> np.ndarray:
        """
        Sắp xếp 4 điểm theo thứ tự:

            top-left
            top-right
            bottom-right
            bottom-left
        """

        pts = np.asarray(pts, dtype=np.float32)

        rect = np.zeros((4, 2), dtype=np.float32)

        s = pts.sum(axis=1)

        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)

        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    @staticmethod
    def four_point_transform(
        image: np.ndarray,
        pts: np.ndarray
    ) -> np.ndarray:
        """
        Perspective Transform từ 4 điểm.
        """

        rect = PerspectiveTransform.order_points(pts)

        tl, tr, br, bl = rect

        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)

        maxWidth = int(max(widthA, widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)

        maxHeight = int(max(heightA, heightB))

        maxWidth = max(maxWidth, 1)
        maxHeight = max(maxHeight, 1)

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype=np.float32)

        matrix = cv2.getPerspectiveTransform(rect, dst)

        warped = cv2.warpPerspective(
            image,
            matrix,
            (maxWidth, maxHeight),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )

        return warped

    @staticmethod
    def transform(
        image: np.ndarray,
        polygon: np.ndarray
    ) -> np.ndarray:
        """
        Perspective Transform từ polygon YOLO Segmentation.

        Parameters
        ----------
        image : np.ndarray
            Ảnh gốc.

        polygon : np.ndarray
            Polygon (N,2) từ YOLO Segmentation.

        Returns
        -------
        np.ndarray
            Ảnh CCCD sau khi được nắn thẳng.
        """

        if image is None:
            raise ValueError("Input image is None.")

        if polygon is None:
            raise ValueError("Polygon is None.")

        polygon = np.asarray(
            polygon,
            dtype=np.float32
        )

        if len(polygon) < 4:
            raise ValueError("Polygon must contain at least 4 points.")

        rect = cv2.minAreaRect(polygon)

        box = cv2.boxPoints(rect).astype(np.float32)

        return PerspectiveTransform.four_point_transform(
            image,
            box
        )