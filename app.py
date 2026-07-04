"""
Drone Crack Detection System - Streamlit UI
Run with:  streamlit run app.py

Camera source: DJI Tello drone ONLY (webcam / USB / IP camera removed).
"""

import os
import time
from datetime import datetime

import cv2
import streamlit as st

import config
import db_control
from drone_camera import DroneCamera
from preprocess import preprocess_frame
from detect import load_model, run_inference, get_severity
from utils.fps import FPSCounter
from utils.draw_boxes import draw_boxes

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(page_title="Drone Crack Detection System", page_icon="🚁", layout="wide")


@st.cache_resource
def get_model():
    return load_model()


model = get_model()

# ----------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------
if "drone" not in st.session_state:
    st.session_state.drone = DroneCamera()
if "drone_connected" not in st.session_state:
    st.session_state.drone_connected = False
if "live_feed" not in st.session_state:
    st.session_state.live_feed = False
if "mongo_enabled" not in st.session_state:
    st.session_state.mongo_enabled = False
if "mysql_enabled" not in st.session_state:
    st.session_state.mysql_enabled = False
if "fps_counter" not in st.session_state:
    st.session_state.fps_counter = FPSCounter()
if "status_msg" not in st.session_state:
    st.session_state.status_msg = ""

# ----------------------------------------------------------------------
# Title
# ----------------------------------------------------------------------
st.title("🚁 Drone Crack Detection System")
st.caption("Real-time road crack detection using YOLOv8 - DJI Tello live feed only")

# ----------------------------------------------------------------------
# Control buttons
# ----------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    connected = st.session_state.drone_connected
    label = "🔴 Disconnect Drone" if connected else "🟢 Connect Drone"
    if st.button(label, key="btn_drone", use_container_width=True):
        if not connected:
            ok, msg = st.session_state.drone.connect()
            st.session_state.drone_connected = ok
        else:
            ok, msg = st.session_state.drone.disconnect()
            st.session_state.drone_connected = False
            st.session_state.live_feed = False
        st.session_state.status_msg = msg
    st.markdown(f"Status: {'🟢 Connected' if st.session_state.drone_connected else '🔴 Disconnected'}")

with col2:
    live = st.session_state.live_feed
    label = "⏸️ Live Feed OFF" if live else "▶️ Live Feed ON"
    if st.button(label, key="btn_live", use_container_width=True, disabled=not st.session_state.drone_connected):
        st.session_state.live_feed = not live
    st.markdown(f"Status: {'🟢 ON' if st.session_state.live_feed else '🔴 OFF'}")

with col3:
    mongo_on = st.session_state.mongo_enabled
    label = "🛢️ MongoDB: ON" if mongo_on else "🛢️ MongoDB: OFF"
    if st.button(label, key="btn_mongo", use_container_width=True):
        st.session_state.mongo_enabled = not mongo_on
    st.markdown(f"Status: {'🟢 Saving' if st.session_state.mongo_enabled else '🔴 Not saving'}")

with col4:
    mysql_on = st.session_state.mysql_enabled
    label = "🛢️ MySQL: ON" if mysql_on else "🛢️ MySQL: OFF"
    if st.button(label, key="btn_mysql", use_container_width=True):
        st.session_state.mysql_enabled = not mysql_on
    st.markdown(f"Status: {'🟢 Saving' if st.session_state.mysql_enabled else '🔴 Not saving'}")

if st.session_state.status_msg:
    st.info(st.session_state.status_msg)

battery = st.session_state.drone.get_battery()
if battery is not None:
    st.sidebar.metric("🔋 Drone Battery", f"{battery}%")
st.sidebar.write("Model:", os.path.basename(config.MODEL_PATH))
st.sidebar.write("Confidence threshold:", config.CONF_THRESHOLD)

st.divider()

# ----------------------------------------------------------------------
# Live feed + detection
# ----------------------------------------------------------------------
frame_placeholder = st.empty()
info_placeholder = st.empty()

if st.session_state.live_feed and st.session_state.drone_connected:
    # NOTE: we intentionally do NOT call st.rerun() on every frame here.
    # Re-running the whole script per-frame reloads the entire page and
    # causes flicker + scroll jumping. Instead we loop in-place and only
    # update the two placeholders (video + info) each iteration.
    # Clicking any button (Live Feed OFF, Disconnect, etc.) automatically
    # interrupts this loop and restarts the script with the new state.
    consecutive_empty_frames = 0
    MAX_EMPTY_FRAMES = 60  # ~2 seconds of no frames before we give up

    while st.session_state.live_feed and st.session_state.drone_connected:
        raw_frame = st.session_state.drone.get_frame()
        frame = preprocess_frame(raw_frame)

        if frame is None:
            consecutive_empty_frames += 1
            if consecutive_empty_frames >= MAX_EMPTY_FRAMES:
                info_placeholder.warning("Lost the drone video feed. Try toggling Live Feed / reconnecting.")
                st.session_state.live_feed = False
                break
            time.sleep(0.03)
            continue

        consecutive_empty_frames = 0
        boxes, class_names = run_inference(model, frame)
        fps = st.session_state.fps_counter.update()
        annotated = draw_boxes(frame.copy(), boxes, class_names)

        frame_placeholder.image(
            cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
            channels="RGB",
            use_container_width=True,
        )

        if boxes:
            best = max(boxes, key=lambda b: b["conf"])
            severity = get_severity(best["conf"])
            crack_type = class_names.get(best["cls"], "Unknown")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            image_name = f"frame_{int(time.time() * 1000)}.jpg"
            image_path = os.path.join(config.UPLOADS_DIR, image_name)
            cv2.imwrite(image_path, annotated)

            data = {
                "camera_id": config.CAMERA_ID,
                "timestamp": timestamp,
                "crack_type": crack_type,
                "severity": severity,
                "confidence": best["conf"],
                "fps": fps,
                "latitude": None,
                "longitude": None,
                "image_path": f"uploads/{image_name}",
            }

            db_control.save_detection(
                data,
                mysql_enabled=st.session_state.mysql_enabled,
                mongo_enabled=st.session_state.mongo_enabled,
            )

            info_placeholder.markdown(
                f"**Crack Type:** {crack_type}  |  **Severity:** {severity}  |  "
                f"**Confidence:** {best['conf']:.2f}  |  **FPS:** {fps}"
            )
        else:
            info_placeholder.markdown(f"No crack detected right now.  |  **FPS:** {fps}")

        time.sleep(0.03)
else:
    frame_placeholder.info("Live feed is OFF, or the drone is not connected. Use the buttons above to start.")
