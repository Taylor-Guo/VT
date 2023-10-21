import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np

# 创建Socket客户端
client_socket = socket.socket()
client_socket.connect(('192.168.137.77', 8000))  # 根据树莓派的IP地址填写

# 创建OpenCV视频窗口
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

try:
    stream = io.BytesIO()
    for _ in range(200):  # 接收200帧视频，可以根据需要调整
        # 从Socket接收视频流数据
        stream_data = client_socket.recv(1024)
        if not stream_data:
            break
        stream.write(stream_data)
        stream.seek(0)

        # 从流中读取视频帧
        image = Image.open(stream)
        frame = np.array(image)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    client_socket.close()
