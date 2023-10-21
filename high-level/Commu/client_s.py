#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
file: client.py
socket client
"""

import socket
import sys


def socket_client(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(s.recv(1024))
    while 1:
        data = input('please input work: ')
        s.send(data.encode())
        print(s.recv(1024))
        if data == 'exit':
            break
    s.close()


if __name__ == '__main__':
    HOST = '192.168.137.147'
    PORT = 6666
    socket_client(HOST, PORT)
