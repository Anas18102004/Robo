#!/usr/bin/env python3
from flask import Flask, Response
import cv2

app = Flask(__name__)

@app.route('/capture', methods=['GET'])
def capture_frame():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Could not open camera", 500

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Failed to capture image", 500

    # Resize to smaller resolution if you want:
    # frame = cv2.resize(frame, (640, 480))

    # Encode frame as JPEG
    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        return "Failed to encode image", 500

    return Response(jpeg.tobytes(), mimetype='image/jpeg')

if __name__ == '__main__':
    # Run on all interfaces so n8n can reach it
    app.run(host='0.0.0.0', port=5000)
