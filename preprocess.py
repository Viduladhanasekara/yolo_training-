import cv2


def preprocess_frame(frame, target_width=640):
    """Resize frame while keeping aspect ratio (keeps YOLO input consistent)."""
    if frame is None:
        return None
    h, w = frame.shape[:2]
    if w == 0:
        return None
    scale = target_width / w
    resized = cv2.resize(frame, (target_width, int(h * scale)))
    return resized