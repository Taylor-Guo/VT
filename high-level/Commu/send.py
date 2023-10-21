#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
file: send.py
socket client
"""

import socket
import os
import sys
import struct
import threading


def socket_client(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((host, port))
        s.listen(2)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    conn.send('Hi, Welcome to the server!'.encode())

    while 1:
        data = conn.recv(1024)
        print('{0} client send data is {1}'.format(addr, data.decode()))
        if data == 'exit' or not data:
            print('{0} connection close'.format(addr))
            conn.send('Connection closed!')
            break
        if data == 'picture':
            filepath = 'test.jpg'
            if os.path.isfile(filepath):
                # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
                fileinfo_size = struct.calcsize('128sl')
                # 定义文件头信息，包含文件名和文件大小
                fhead = struct.pack(
                    fileinfo_size,
                    bytes(os.path.basename(filepath), encoding='utf-8'),
                    os.stat(filepath).st_size)
                conn.send(fhead)
                print('client filepath: {0}'.format(filepath))

                fp = open(filepath, 'rb')
                while 1:
                    pic = fp.read(1024)
                    if not pic:
                        print('{0} file send over...'.format(filepath))
                        break
                    conn.send(pic)
        conn.close()
        break


if __name__ == '__main__':
    HOST = '192.168.137.147'
    PORT = 6666
    socket_client(HOST, PORT)
