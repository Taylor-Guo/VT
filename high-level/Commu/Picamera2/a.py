import cv2

cap = cv2.VideoCapture(0)

cap.set(3, 320)  # width of the image 320
cap.set(4, 240)  # height of the image 240
cap.set(5, 60)  # framerate 60

print(cap.get(3))
print(cap.get(4))
print(cap.get(5))

for i in range(60):
    ret, color_frame = cap.read()
    img1 = cv2.flip(color_frame, 0)  # flip image, 0 vertically, 1 horizontally
    cv2.imwrite(f'/home/pi/work/camera_module/pic/test{i}.jpg', img1)
    cv2.imshow(f'test{i}', img1)
    print(f'Currently, the {i}th pictures')
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
