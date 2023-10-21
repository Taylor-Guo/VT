import cv2
import numpy as np
import socket

# Define constants
img_size = 640 * 480 * 3  # Image size (3 channels for color)
raspi_ip = "169.254.50.11"
port = 1234

# Initialize a socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((raspi_ip, port))
print("Connected to the server")

while True:
    try:
        # Receive image data
        img_data = b""
        bytes_received = 0
        while bytes_received < img_size:
            chunk = client_socket.recv(img_size - bytes_received)
            if chunk == b'':
                raise ConnectionError("Connection to the server was lost")
            img_data += chunk
            bytes_received += len(chunk)

        # Receive center point data
        point_data = client_socket.recv(8)  # Assuming 2 integers for x and y

        # Convert image data to a NumPy array
        img_np = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        # Extract center coordinates
        x, y = struct.unpack('ii', point_data)  # Assuming little-endian format

        # Draw a circle at the center point
        cv2.circle(img, (x, y), 6, (0, 255, 0), -1)

        # Display the image
        cv2.imshow("Gray_Center", img)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        break

# Close the socket connection
client_socket.close()
cv2.destroyAllWindows()
