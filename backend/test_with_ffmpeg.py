import sys
import tty
import termios
import time
import threading
import ffmpeg

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)



def get_image():
    process = (
        ffmpeg
        .input("rtsp://localhost:8554/mystream")
        .output("pipe:", format="rawvideo", pix_fmt="rgb24")
        .run_async(pipe_stdout=True)
    )
    while True:
        frame = process.stdout.read(WIDTH * HEIGHT * 3)
        if not frame:
            break
        # store frame in memory
        

t = threading.Thread(target=get_image, args=(), kwargs={})

t.start()
print("press q to stop")
while True:
    
    key = get_key()
    if key == 'q':
        t.join()