"""
Core YOLOv8 detection logic - reusable by the Streamlit app (app.py).
Loads model/best.pt exactly as-is; no changes to how the model was trained.
"""

from ultralytics import YOLO
import config


def load_model():
    return YOLO(config.MODEL_PATH)


def run_inference(model, frame):
    """
    Run YOLOv8 on a single frame.
    Returns: (boxes, class_names)
      boxes: list of dicts [{x1,y1,x2,y2,conf,cls}, ...]
      class_names: dict {class_id: class_name}
    """
    results = model.predict(frame, conf=config.CONF_THRESHOLD, verbose=False)
    boxes_out = []
    class_names = model.names

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            boxes_out.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2, "conf": conf, "cls": cls_id})

    return boxes_out, class_names


def get_severity(confidence: float) -> str:
    if confidence >= config.SEVERITY_HIGH:
        return "High"
    elif confidence >= config.SEVERITY_MEDIUM:
        return "Medium"
    return "Low"