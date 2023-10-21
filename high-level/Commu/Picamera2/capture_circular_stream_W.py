import cv2
import socket
import numpy as np

# 创建一个UDP socket
server_address = ('192.168.137.77', 10001)  # 这里可以根据需要设置IP地址和端口
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

# 创建OpenCV视频窗口
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

motion_detected = False
last_motion_time = None

while True:
    data, address = sock.recvfrom(65535)

    # 接收到视频数据
    if data.startswith(b'\xff\xd8') and data.endswith(b'\xff\xd9'):
        # 解码JPEG图像
        frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('Video', frame)

    # 接收到运动检测信息
    elif data.startswith(b'Motion Detected:'):
        motion_detected = True
        last_motion_time = data.decode('utf-8').split(': ')[1]

    # 检查并显示运动检测信息
    if motion_detected:
        if last_motion_time:
            cv2.putText(frame, f"Motion Detected at {last_motion_time}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            last_motion_time = None
        cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 清理
cv2.destroyAllWindows()
sock.close()
