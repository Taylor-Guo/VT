import socket
import struct
import cv2
import numpy as np

# 设置服务器IP地址和端口
server_ip = '10.185.216.246'  # 将其更改为您的Windows电脑的IP地址
server_port = 8000

# 创建Socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口
server_socket.bind((server_ip, server_port))

# 开始监听连接
server_socket.listen(0)

print(f"等待连接中...")

# 等待客户端连接
client_socket, addr = server_socket.accept()
print(f"连接来自 {addr}")

# 创建一个OpenCV窗口用于显示图像
cv2.namedWindow("Raspberry Pi Camera", cv2.WINDOW_NORMAL)

try:
    while True:
        # 接收图像大小信息（4个字节）
        image_size_data = client_socket.recv(4)
        if not image_size_data:
            break
        # 解包图像大小
        image_size = struct.unpack('<L', image_size_data)[0]

        # 接收图像数据
        image_data = b''
        while len(image_data) < image_size:
            chunk = client_socket.recv(image_size - len(image_data))
            if not chunk:
                raise Exception("接收图像数据失败")
            image_data += chunk

        # 将接收到的数据转换为图像
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # 显示图像
        cv2.imshow("Raspberry Pi Camera", image)

        # 检测按键 "q" 是否被按下，如果是则退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 关闭连接和窗口
    client_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()
