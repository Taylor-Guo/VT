#!/usr/bin/python3
import io
import socket
import struct
import time
import picamera2
from picamera2 import PiCameraCircularIO

# 创建PiCamera对象
picam = picamera2.Picamera2()
picam.resolution = (640, 480)  # 设置视频分辨率
picam.framerate = 120  # 设置帧率
output = PiCameraCircularIO(picam, seconds=10)  # 创建循环视频缓冲区

# 开始录制视频到循环缓冲区
picam.start_recording(output, format='h264')

# 创建一个Socket服务器
server_socket = socket.socket()
server_socket.bind(('192.168.137.77', 8000))  # 绑定到树莓派上的IP和端口
server_socket.listen(0)
print("等待连接...")

# 接受连接
connection = server_socket.accept()[0]
print("连接建立")

try:
    while True:
        # 从循环缓冲区读取数据
        output.copy_to(connection.makefile('wb'))
        output.clear()

finally:
    connection.close()
    server_socket.close()
    picam.stop_recording()
