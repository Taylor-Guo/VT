#!/usr/bin/python3
import socket
import threading
import time

import numpy as np

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput, FileOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (640, 480), "format": "RGB888"})
picam2.configure(video_config)
encoder = H264Encoder(1000000)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect(('192.169.137.77', 10001))
    stream = sock.makefile("wb")
    picam2.start_recording(encoder, FileOutput(stream))
    time.sleep(20)
    picam2.stop_recording()
