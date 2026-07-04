"""
DJI Tello drone camera controller.
Handles connect / disconnect / live video stream from the Tello drone ONLY.
(No webcam / USB / IP camera support - per project requirement.)
"""

import cv2
from djitellopy import Tello


class DroneCamera:
    def __init__(self):
        self.tello = None
        self.connected = False
        self.streaming = False

    def connect(self):
        """Connect to the DJI Tello drone and start its video stream."""
        if self.connected:
            return True, "Drone is already connected."
        try:
            self.tello = Tello()
            self.tello.connect()
            battery = self.tello.get_battery()
            self.tello.streamon()
            self.connected = True
            self.streaming = True
            return True, f"Connected to DJI Tello. Battery: {battery}%"
        except Exception as e:
            self.connected = False
            self.tello = None
            return False, f"Failed to connect to drone: {e}"

    def disconnect(self):
        """Stop the stream and disconnect from the drone."""
        if not self.connected:
            return True, "Drone is already disconnected."
        try:
            if self.tello is not None:
                try:
                    self.tello.streamoff()
                except Exception:
                    pass
                self.tello.end()
        except Exception as e:
            return False, f"Error while disconnecting: {e}"
        finally:
            self.tello = None
            self.connected = False
            self.streaming = False
        return True, "Drone disconnected."

    def get_frame(self):
        """Return one BGR frame from the drone's live feed, or None."""
        if not self.connected or self.tello is None:
            return None
        try:
            frame_reader = self.tello.get_frame_read()
            frame = frame_reader.frame
            if frame is None:
                return None
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            return frame
        except Exception:
            return None

    def get_battery(self):
        if self.connected and self.tello is not None:
            try:
                return self.tello.get_battery()
            except Exception:
                return None
        return None