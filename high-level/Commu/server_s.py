#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
file: service.py
socket service
"""

import socket
import threading
import time
import sys


def socket_service(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
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
    welcome = 'Hi, Welcome to the server!'.encode()
    conn.send(welcome)
    while 1:
        data = conn.recv(1024).decode()
        print('{0} client send data is {1}'.format(addr, data))
        time.sleep(1)
        if data == 'exit' or not data:
            print('{0} connection close'.format(addr))
            conn.send('Connection closed!')
            break
        string = 'Hello, {0}'.format(data)
        conn.send(string.encode())
    conn.close()


if __name__ == '__main__':
    HOST = '192.168.137.147'
    PORT = 6666
    socket_service(HOST, PORT)
