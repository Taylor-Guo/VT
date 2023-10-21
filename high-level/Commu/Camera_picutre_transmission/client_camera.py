#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import os
import sys
import struct
from picamera2 import Picamera2

# import time


# raspberry pi as the client of the socket
def socket_client(host, port, num=5):
    cam = Picamera2()
    cam.resolution(640, 480)
    cam.framerate = 30
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print(s.recv(1024))

    while 1:
        for i in range(num):
            filepath = '/home/pi/work/Picamera_test/pictures/test%s.jpg' % i
            cam.capture(filepath)
            if os.path.isfile(filepath):
                # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
                # fileinfo_size = struct.calcsize('128sl')
                # 定义文件头信息，包含文件名和文件大小
                fhead = struct.pack(
                    b'128sl',
                    bytes(os.path.basename(filepath).encode('utf-8')),
                    os.stat(filepath).st_size)
                s.send(fhead)
                print('client filepath: {0}'.format(filepath))

                fp = open(filepath, 'rb')
                while 1:
                    data = fp.read(1024)
                    if not data:
                        print('{0} file send over...'.format(filepath))
                        break
                    s.send(data)
        s.close()
        break


if __name__ == '__main__':
    # HOST = '192.168.137.147'  # Raspberry Pi 连接本地服务器，可通过ipconfig/all看IPV4的地址
    HOST = '10.185.228.206'  # PC
    PORT = 2222  # 设置端口号，自己设置即可
    socket_client(HOST, PORT)
