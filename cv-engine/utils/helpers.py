import base64

import cv2
import numpy as np


def base64_to_frame(image_base64):
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    raw = base64.b64decode(image_base64)
    np_buffer = np.frombuffer(raw, np.uint8)
    frame = cv2.imdecode(np_buffer, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("Invalid image payload")
    return frame
