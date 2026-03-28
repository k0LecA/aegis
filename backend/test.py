import cv2

cap = cv2.VideoCapture('/home/shark/roll.mp4', cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

print(cap.isOpened())

while True:
    ret, frame = cap.read()

    if not ret:
        break   # No more frames → end of video

    cv2.imshow("Video", frame)

    # Press Q to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()

print(cap.isOpened())