FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ffmpeg curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download YOLOv8n model during build (requires internet at build time)
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

COPY . .
RUN mkdir -p data/videos data/sales data/outputs