import cv2
import socket
import numpy as np

# 创建一个UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('192.168.137.77', 10001))  # 这里的端口要与树莓派端的设置相匹配

# 创建OpenCV视频窗口
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

while True:
    data, _ = client_socket.recvfrom(65535)

    # 解码JPEG图像
    if data.startswith(b'\xff\xd8') and data.endswith(b'\xff\xd9'):
        frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 清理
cv2.destroyAllWindows()
client_socket.close()
