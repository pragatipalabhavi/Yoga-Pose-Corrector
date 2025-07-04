from flask import Flask, render_template, Response, url_for, request, redirect, jsonify
from flask_socketio import SocketIO, emit
import YogaPose
import mediapipe as mp
import cv2
import os
import heatmap
import threading
import pyttsx3
import ollama

app = Flask(__name__)
socket = SocketIO(app)

# Global variables
global yogaPose
global genHeatMap 

def landVal(i, j):
    position_mapping = {
        (0, 1): 13,  # left elbow
        (0, 2): 14,  # right elbow
        (1, 1): 26,  # right knee
        (1, 2): 27,  # left knee
        (2, 1): 12,  # right shoulder
        (2, 2): 11,  # left shoulder
        (3, 1): 23,  # left hip
        (3, 2): 24   # right hip
    }
    return position_mapping.get((i, j), 0)

def checkPoseCompletion(bool_list):
    return all(result[0] for result in bool_list)

class CamInput:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.camera = cv2.VideoCapture(0)
        self.obj = YogaPose.MatchYogaPos()
        
        # Video settings
        self.height, self.width = 640, 480  # Changed to standard webcam resolution
        self.text = 'good'
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.color_correct = (0, 255, 0)  # Green in BGR
        self.color_incorrect = (0, 0, 255)  # Red in BGR
        
        # State flags
        self.isPoseCorrect = False
        self.done = False
        self.frame_count = 0

    def genHeatMap(self, tempList):
        obj = heatmap.heatMap()
        obj.createHeatmap(tempList)

    def speak(self, tempList):
        if not tempList:
            return
            
        parts = []
        body_parts = {
            0: "elbow",
            1: "knee",
            2: "shoulder",
            3: "hip",
        }

        for i in range(4):
            if not tempList[i][0]:
                parts.append(body_parts[i])
        
        if not parts:
            return
        
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            
            if len(parts) > 1:
                message = f'Correct your {", ".join(parts[:-1])} and {parts[-1]}'
            else:
                message = f'Correct your {parts[0]}'
            
            engine.say(message)
            engine.runAndWait()
        except Exception as e:
            print(f"Text-to-speech error: {e}")

    def gen_frames(self, socket):
        global genHeatMap
        genHeatMap = False
        
        with self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
            while self.camera.isOpened():
                success, frame = self.camera.read()
                if not success:
                    break

                # Resize frame to standard dimensions
                frame = cv2.resize(frame, (self.width, self.height))
                
                # Create a copy for processing
                image = frame.copy()
                
                # Convert to RGB for Mediapipe
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image_rgb.flags.writeable = False
                results = pose.process(image_rgb)
                image_rgb.flags.writeable = True
                
                temp_list = None

                if results.pose_landmarks:
                    temp_list = self.obj.matchYogaPos(results.pose_landmarks.landmark, yogaPose)
                    
                    if not self.isPoseCorrect and temp_list and checkPoseCompletion(temp_list):
                        self.isPoseCorrect = True
                        socket.emit('complete')

                    # Draw landmarks on the original frame
                    self.mp_drawing.draw_landmarks(
                        frame,  # Draw on original frame
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                        self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                    )
                    
                    # Add text annotations
                    for i in range(4):
                        if temp_list and len(temp_list) > i:
                            if temp_list[i][0]:
                                color = self.color_correct
                                text = self.text
                            else:
                                color = self.color_incorrect
                                text = str(round(temp_list[i][1]))
                            
                            for j in [1, 2]:
                                landmark_idx = landVal(i, j)
                                if landmark_idx and results.pose_landmarks.landmark[landmark_idx]:
                                    x = int(results.pose_landmarks.landmark[landmark_idx].x * self.width) + 3
                                    y = int(results.pose_landmarks.landmark[landmark_idx].y * self.height) + 3
                                    cv2.putText(frame, text, (x, y), self.font, 0.5, 
                                              color, 1, cv2.LINE_AA)

                # Generate heatmap if requested
                if genHeatMap and not self.done and temp_list:
                    self.genHeatMap(temp_list)
                    self.done = True

                # Audio feedback every 100 frames (~3-4 seconds)
                self.frame_count += 1
                if self.frame_count % 100 == 0 and temp_list:
                    threading.Thread(target=self.speak, args=(temp_list,)).start()

                # Encode the frame in JPEG format
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def close_cam(self):
        self.camera.release()

# Flask Routes (remain the same as previous version)
@app.route('/')
def home():
    return render_template('index.html', json_url=url_for('static', filename='json/pose_details.json'))

@app.route('/perform', methods=['POST'])
def perform():
    global yogaPose
    yogaPose = request.form.get('selected_pose')
    return redirect(url_for('yoga'))

@app.route('/yoga')
def yoga():
    global cam_obj
    cam_obj = CamInput()
    return render_template('yoga.html', pose=yogaPose, poseComplete=cam_obj.isPoseCorrect)

@app.route('/video_feed')
def video_feed():
    return Response(cam_obj.gen_frames(socket), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/close_webcam', methods=['POST'])
def close_webcam():
    cam_obj.close_cam()
    return "Webcam Closed"

# SocketIO Handlers (remain the same as previous version)
@socket.on('send_message')
def handle_message(data):
    try:
        user_input = data.get('message', '').strip()
        if not user_input:
            emit('receive_message', {'message': "Please enter a valid message."})
            return

        response = ollama.chat(
            model='mistral',
            messages=[{"role": "user", "content": user_input}]
        )
        bot_message = response.get('message', {}).get('content', 'I could not generate a response.')
        emit('receive_message', {'message': bot_message})
    except Exception as e:
        print(f"Chat error: {e}")
        emit('receive_message', {'message': "An error occurred while processing your request."})

@socket.on('heatmap')
def handle_heatmap():
    global genHeatMap
    genHeatMap = True

@socket.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == "__main__":
    socket.run(app, allow_unsafe_werkzeug=True, debug=True)