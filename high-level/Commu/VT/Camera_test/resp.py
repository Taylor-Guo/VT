import cv2
from picamera2 import Picamera2
import time
import socket
import struct
import numpy as np

# 设置树莓派相机
picam2 = Picamera2()
picam2.start()
time.sleep(1)
print(f'Camera has been started')

try:
    client_socket = socket.socket()
    client_socket.connect(('10.185.216.246', 8000))  # Replace with the actual Windows computer's IP address

    # If the code reaches here, the connection was successful
    print("Connected to the Windows computer.")

    try:
        while True:
            array = picam2.capture_array("main")
            print(f'image captured, size {array.shape}')
            # 转换 Numpy 数组为 JPEG 格式的图像
            image_data = cv2.imencode('.jpg', array)[1].tobytes()

            # 发送图像到 Windows 电脑
            connection = client_socket.makefile('wb')
            connection.write(struct.pack('<L', len(image_data)))
            connection.write(image_data)
            connection.flush()
            connection.close()

            frame_count += 1
            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time > 1.0:  # 打印每秒的帧数和发送频率
                print(f"这是第 {frame_count} 帧，发送频率: {frame_count / elapsed_time:.2f} 帧/秒")
                frame_count = 0
                start_time = time.time()

    finally:
        client_socket.close()


except ConnectionRefusedError:
    print("Connection was refused. Please check the server address and port.")
except Exception as e:
    print(f"An error occurred while connecting: {str(e)}")
    # Handle any other exceptions as needed


