# app.py
from flask import Flask, Response
import cv2
import threading
import time

app = Flask(__name__)
# 
rtsp_url = "rtsp://admin:admin@192.168.31.99:554/stream2"

frame_lock = threading.Lock()
latest_frame = None
running = True

def rtsp_worker():
    global latest_frame, running
    while running:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            print("无法连接RTSP流，5秒后重试...")
            time.sleep(5)
            continue
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("读取帧失败，重连中...")
                break
            with frame_lock:
                ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                if ret:
                    latest_frame = jpeg.tobytes()
        cap.release()
        time.sleep(1)

def generate_mjpeg():
    global latest_frame
    while True:
        with frame_lock:
            if latest_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
        time.sleep(0.05)  # 控制帧率

@app.route('/video_feed')
def video_feed():
    return Response(generate_mjpeg(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    threading.Thread(target=rtsp_worker, daemon=True).start()
    app.run(host='0.0.0.0', port=5589, threaded=True)

