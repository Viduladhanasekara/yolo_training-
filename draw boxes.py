import cv2


def draw_boxes(frame, boxes, class_names):
    """
    Draw bounding boxes with label + confidence on the frame.
    boxes: list of dicts {x1,y1,x2,y2,conf,cls}
    """
    for box in boxes:
        x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
        conf = box["conf"]
        cls_id = box["cls"]
        label = class_names.get(cls_id, str(cls_id))

        if conf >= 0.80:
            color = (0, 0, 255)       # red - high severity
        elif conf >= 0.55:
            color = (0, 165, 255)     # orange - medium severity
        else:
            color = (0, 255, 255)     # yellow - low severity

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        text = f"{label} {conf:.2f}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 4, y1), color, -1)
        cv2.putText(frame, text, (x1 + 2, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return frame