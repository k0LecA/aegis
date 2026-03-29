import threading
import time
import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import os

file = open("camsource.txt", "r")
camsource=file.read()

class CameraSystem:
    def __init__(self):
        self.stop_event = threading.Event()
        self.thread = None
        self.current_frame = None

        self.camera_source = camsource

    def capture_loop(self):
        #os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
        cap = cv2.VideoCapture(self.camera_source)
        #cap = cv2.VideoCapture(self.camera_source, cv2.CAP_FFMPEG)
        print("[AEGIS] Optical sensors initialized.")

        #show latest frame (some frame loss)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        #ask server for this
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while not self.stop_event.is_set():
            success, frame = cap.read()
            if success:
                #resize
                small_frame = cv2.resize(frame, (190, 60), interpolation=cv2.INTER_AREA)
                _, buffer = cv2.imencode('.jpg', small_frame, [cv2.IMWRITE_JPEG_QUALITY, 20])
                self.current_frame = buffer.tobytes()
            else:
                print("[AEGIS] Warning: Connection lost. Retrying...")
                time.sleep(1)
        
        cap.release()
        print("[AEGIS] Camera thread safely terminated.")

aegis = CameraSystem()

@asynccontextmanager
async def lifespan(app: FastAPI):
    aegis.thread = threading.Thread(target=aegis.capture_loop, daemon=True)
    aegis.thread.start()
    yield
    print("[AEGIS] Shutting down. Waiting for background tasks...")
    aegis.stop_event.set()
    aegis.thread.join(timeout=2.0)
    print("[AEGIS] Goodbye, testing candidate.")

app = FastAPI(lifespan=lifespan)



@app.get("/")
async def root():
    return {"status": "Online", "system": "AEGIS"}

def frame_generator():
    while not aegis.stop_event.is_set():
        if aegis.current_frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + aegis.current_frame + b'\r\n')
        time.sleep(0.04)

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(
        frame_generator(), 
        media_type="multipart/x-mixed-replace; boundary=frame"
    )