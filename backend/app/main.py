import threading
import time
import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager

file = open("camsource.txt", "r")
camsource=file.read()

class CameraSystem:
    def __init__(self):
        self.stop_event = threading.Event()
        self.thread = None
        self.current_frame = None

        self.camera_source = camsource

    def capture_loop(self):
        cap = cv2.VideoCapture(self.camera_source)
        print("[AEGIS] Optical sensors initialized.")
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while not self.stop_event.is_set():
            success, frame = cap.read()
            if success:

                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
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