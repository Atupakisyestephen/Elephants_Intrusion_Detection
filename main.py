from ultralytics import YOLO
import cv2
import pygame
import threading
from flask import Flask, Response, render_template, jsonify
from flask_socketio import SocketIO, emit
import time
import csv
import os

# Initialize pygame mixer
pygame.mixer.init()

# Load the model
model = YOLO("yolov8n.pt")

# Load the video
video_path = 'elephant.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Unable to open video file {video_path}")
    exit()

# Elephant class index
elephant_class_index = 5

# Alarm state
alarm_playing = False
alarm_lock = threading.Lock()

# Flask app
app = Flask(__name__)
socketio = SocketIO(app)

# Detection history
detection_history = []

# Ensure detection log file exists
log_file = 'detection_log.csv'
if not os.path.exists(log_file):
    with open(log_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Details", "Latitude", "Longitude"])

def play_alarm():
    pygame.mixer.music.load('alarm_sound.mp3')
    pygame.mixer.music.play(-1)  # Play in a loop

def stop_alarm():
    pygame.mixer.music.stop()

def generate_frames():
    global alarm_playing
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLO model on the frame
        results = model(frame)
        
        # Flag to check if an elephant is detected
        elephant_detected = False
        
        # Iterate through results and draw annotations on the frame
        for result in results:
            annotated_frame = result.plot()
            for box in result.boxes:
                if int(box.cls) == elephant_class_index:  # Check if the detected class is an elephant
                    elephant_detected = True

        # Play or stop alarm based on detection
        with alarm_lock:
            if elephant_detected:
                if not alarm_playing:
                    threading.Thread(target=play_alarm).start()
                    alarm_playing = True
                    detection_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    detection_details = f"Elephant detected at {detection_time}"
                    detection_history.append({
                        "time": detection_time,
                        "latitude": -1.286389,  # Example latitude
                        "longitude": 36.817223  # Example longitude
                    })
                    socketio.emit('new_detection', {'time': detection_time})
                    
                    # Log detection to CSV
                    with open(log_file, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([detection_time, detection_details, -1.286389, 36.817223])
            else:
                if alarm_playing:
                    stop_alarm()
                    alarm_playing = False
        
        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detection_history')
def get_detection_history():
    return jsonify(detection_history)

@app.route('/analytics')
def analytics():
    # Read detection log data
    detection_data = []
    with open(log_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            detection_data.append(row)
    return render_template('analytics.html', detection_data=detection_data)

@app.route('/map')
def map_view():
    return render_template('map.html')

if __name__ == "__main__":
    socketio.run(app, debug=True)
