# Elephant Intrusion Detection

This project uses the YOLOv8 model to detect elephants in a video stream and trigger an alarm when an elephant is detected. It also logs the detections and provides a web interface to view the live video feed and detection history.

## Features

- Real-time elephant detection using YOLOv8
- Alarm sound when an elephant is detected
- Logging of detection events with timestamp and location
- Web interface to view live video feed and detection history
- Analytics page to view detection data
- Map view to visualize detection locations

## Installation

### Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO
- OpenCV
- Pygame
- Ultralyics YOLO

### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Atupakisyestephen/Elephants_Intrusion_Detection.git
   cd Elephants_Intrusion_Detection
2. Install the required packages:
    pip install -r requirements.txt
3. Ensure you have the YOLOv8 model file (yolov8n.pt) in the project directory. If not, download it from the Ultralytics YOLOv8 repository.
4. Place your video file (e.g., elephant.mp4) in the project directory.
5. Place your alarm sound file (e.g., alarm_sound.mp3) in the project directory.

   Usage
1. Run the Flask application:
   python main.py
2. Open your web browser and go to http://127.0.0.1:5000/ to access the web interface.

   ![elephant1](https://github.com/user-attachments/assets/d4c8d9e5-2feb-4a64-b47d-3dcc59ef4551)
   ![elephant2](https://github.com/user-attachments/assets/67818881-fcaa-4279-98a7-fae2d5889e78)
   ![elephant3](https://github.com/user-attachments/assets/fbc76001-cb3b-47a4-900b-27a9b2f9821d)

   Project Structure
main.py: The main Flask application file.
templates/: Contains HTML templates for the web interface.
static/: Contains static files such as CSS and JavaScript.
requirements.txt: List of required Python packages.

   How It Works
The YOLOv8 model is loaded and used to process frames from the video file.
When an elephant is detected in a frame, an alarm sound is played.
Detection events are logged with a timestamp and location.
The web interface allows users to view the live video feed, detection history, and analytics.

   Routes
/: The homepage displaying the live video feed.
/video_feed: Endpoint providing the live video feed.
/detection_history: Endpoint returning the detection history as JSON.
/analytics: Page displaying detection analytics.
/map: Page displaying a map view of detection locations.

   License
This project is licensed under the MIT License.
