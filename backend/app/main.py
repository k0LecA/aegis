import threading
import time
import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager


class CameraSystem:
    def __init__(self):
        self.stop_event = threading.Event()
        self.thread = None
        self.current_frame = None

        self.camera_source = "rtsp://localhost:8554/test"

    def capture_loop(self):
        cap = cv2.VideoCapture(self.camera_source)
        print("[AEGIS] Optical sensors initialized.")
        
        while not self.stop_event.is_set():
            success, frame = cap.read()
            if success:

                _, buffer = cv2.imencode('.jpg', frame)
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
    aegis.thread.join()
    print("[AEGIS] Goodbye, testing candidate.")

app = FastAPI(lifespan=lifespan)



@app.get("/")
async def root():
    return {"status": "Online", "system": "AEGIS"}

def frame_generator():
    """Генератор, который FastAPI будет 'стримить' в браузер"""
    while True:
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