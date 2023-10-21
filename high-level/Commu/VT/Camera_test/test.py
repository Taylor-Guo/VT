import cv2
import numpy as np
import socket
import struct

USEPORT = 1234
T = 20

def gray_center(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_gray = cv2.threshold(img_gray, T, 255, cv2.THRESH_BINARY)
    M = cv2.moments(img_gray)
    if M["m00"] == 0:
        return (0, 0)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)

def main():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("fail to open camera!")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', USEPORT))
    server_socket.listen(1)

    print("Listening on port", USEPORT)

    client_socket, _ = server_socket.accept()

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        center = gray_center(frame)
        data = frame.tobytes()
        point_data = struct.pack("ii", center[0], center[1])

        client_socket.send(data)
        client_socket.send(point_data)

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
