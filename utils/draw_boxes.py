import cv2


def draw_boxes(frame, boxes, class_names):
    """
    Draw bounding boxes with label + confidence on the frame.
    boxes: list of dicts {x1,y1,x2,y2,conf,cls}

    The label is placed above the box by default, but automatically
    flips to below the box (or clamps horizontally) if it would
    otherwise be drawn outside the visible frame - this prevents the
    crack name from being cut off at the frame edges.
    """
    h, w = frame.shape[:2]

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

        # clamp the box itself to the frame just in case
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        text = f"{label} {conf:.2f}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        pad = 6

        # Vertical placement: above the box, unless there isn't room -
        # then flip to below the box.
        if y1 - th - pad * 2 >= 0:
            label_top = y1 - th - pad * 2
            label_bottom = y1
            text_y = y1 - pad
        else:
            label_top = y2
            label_bottom = min(h - 1, y2 + th + pad * 2)
            text_y = y2 + th + pad

        # Horizontal placement: clamp so the label never spills past
        # the right (or left) edge of the frame.
        label_left = x1
        label_right = x1 + tw + pad
        if label_right > w:
            label_right = w - 1
            label_left = max(0, label_right - tw - pad)

        cv2.rectangle(frame, (label_left, label_top), (label_right, label_bottom), color, -1)
        cv2.putText(frame, text, (label_left + 3, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return frame
