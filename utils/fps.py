import time


class FPSCounter:
    def __init__(self, smoothing=0.9):
        self._prev_time = None
        self._fps = 0.0
        self.smoothing = smoothing

    def update(self):
        now = time.time()
        if self._prev_time is None:
            self._prev_time = now
            return 0.0
        dt = now - self._prev_time
        self._prev_time = now
        if dt > 0:
            current_fps = 1.0 / dt
            self._fps = (self.smoothing * self._fps) + ((1 - self.smoothing) * current_fps)
        return round(self._fps, 1)
