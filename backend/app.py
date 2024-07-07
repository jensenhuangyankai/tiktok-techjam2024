import os
from flask import Flask, Response, request, send_from_directory
from flask_uploads import UploadSet, configure_uploads
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FRAME_FOLDER'] = 'frames'
os.makedirs(app.config['FRAME_FOLDER'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def setDest(app):
    return app.config['UPLOAD_FOLDER']

videos = UploadSet("videos", ["mp4", "mov", "avi", "wmv", "avchd", "webm", "flv"], default_dest=setDest)
configure_uploads(app, videos)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST' and 'video' in request.files:
        filename = videos.save(request.files['video'])
        print("video saved.")
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        frame_files = extract_frames(video_path, app.config['FRAME_FOLDER'])
        print(frame_files)

            

        
        return Response({"yes": "yes"}, status=200, mimetype='application/json')
    else:
        return Response({"no": "no"}, status=201, mimetype='application/json')

@app.route('/frames/<filename>')
def get_frame(filename):
    return send_from_directory(app.config['FRAME_FOLDER'], filename)

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    frame_files = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_files.append(frame_filename)
        frame_count += 1

    cap.release()
    return frame_files
