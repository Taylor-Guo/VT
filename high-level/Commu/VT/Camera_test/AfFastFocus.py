from picamera2 import Picamera2
from libcamera import controls
picam2 = Picamera2()
picam2.start(show_preview=True)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
picam2.start_and_capture_files("fastfocus-test{:d}.jpg", num_files=3, delay=0.5)
picam2.stop_preview()
picam2.stop()