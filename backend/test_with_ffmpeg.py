import sys
import tty
import termios
import threading
import ffmpeg
import os

# Укажите ваши размеры
WIDTH = 640 
HEIGHT = 480

# Флаг для остановки потока
stop_event = threading.Event()

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def get_image():
    # Запускаем ffmpeg
    process = (
        ffmpeg
        .input("rtsp://localhost:8554/mystream")
        .output("pipe:", format="rawvideo", pix_fmt="rgb24")
        .run_async(pipe_stdout=True, pipe_stderr=True) # Добавили stderr для отладки
    )
    
    try:
        while not stop_event.is_set():
            # Читаем ровно один кадр
            frame_size = WIDTH * HEIGHT * 3
            frame = process.stdout.read(frame_size)
            
            if not frame:
                print("\nStream ended or error")
                break
            
            # Здесь ваша логика обработки кадра
            # ...
            
    finally:
        # Важно: убиваем процесс ffmpeg при выходе
        process.terminate()
        process.wait()
        print("\nFFmpeg process stopped")

# Создаем поток как "демона", чтобы он не блокировал выход из Python, если что-то пойдет не так
t = threading.Thread(target=get_image, daemon=True)
t.start()

print("Press 'q' to stop")

try:
    while True:
        key = get_key()
        if key == 'q':
            print("\nStopping...")
            stop_event.set() # Сигнализируем потоку о выходе
            break
finally:
    t.join(timeout=2) # Ждем завершения потока максимум 2 секунды
    print("Done.")