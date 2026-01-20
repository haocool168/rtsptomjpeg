FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mjpeg_stream.py .

RUN apt update && apt install -y ffmpeg libgl1-mesa-glx && \
    pip install flask opencv-python-headless

EXPOSE 5589

CMD ["python3", "mjpeg_stream.py"]
