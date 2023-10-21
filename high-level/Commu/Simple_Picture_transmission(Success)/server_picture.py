#!/usr/bin/env python
# -*- coding=utf-8 -*-
import socket
import threading
# import time
import sys
import os
import struct


# PC as server of the socket
def socket_service(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 这里换上自己的ip和端口
        s.bind((host, port))
        s.listen(2)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Waiting for connection...")

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    welcome = 'Hi, Welcome to the server!'.encode()
    conn.send(welcome)
    while 1:
        fileinfo_size = struct.calcsize(b'128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack(b'128sl', buf)
            # remove the specific head/tail of the string
            fn = filename.strip(str.encode('\00'))
            # PC 端图片保存路径
            new_filename = os.path.join(str.encode('./'),
                                        str.encode('new_') + fn)
            print('file new name is {0}, filesize if {1}'.format(
                new_filename, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print("start receiving...")
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print("end receive...")
        conn.close()
        break


if __name__ == '__main__':
    # HOST = '192.168.137.147'  # Raspberry Pi 连接本地服务器，可通过ipconfig/all看IPV4的地址
    HOST = '10.185.228.206'  # PC
    PORT = 10001  # 设置端口号，自己设置即可
    socket_service(HOST, PORT)
