import os
from flask import Flask, Response, request, send_from_directory, jsonify
from flask_uploads import UploadSet, configure_uploads
import cv2
from werkzeug.utils import secure_filename
import shutil
from PIL import Image

from ImageProcess import *


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FRAME_FOLDER'] = 'frames'
os.makedirs(app.config['FRAME_FOLDER'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
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


nounList = []
with open("common-nouns.txt", 'r') as file:
    lines = file.readlines()
    for line in lines:
        word = line.strip()
        nounList.append(word)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST' and 'video' in request.files:
        filename = videos.save(request.files['video'])
        print("video saved.")
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        frame_folder = os.path.join(app.config['FRAME_FOLDER'], filename)
        frame_files = extract_frames(video_path, frame_folder)
        
        frame_num = 0
        imageTags = {word: 0 for word in nounList}
        cumulative_sums = {key: 0 for key in imageTags}
        counts = {key: 0 for key in imageTags}

        for i in range(0, len(frame_files), 10):
            print(frame_num)
            
            frame_file = frame_files[i]
            image = Image.open(frame_file)
            newImageTags = getImageTags(image, nounList)

            for key in newImageTags:
                cumulative_sums[key] += newImageTags[key]
                counts[key] += 1
            avg_dict = {key: cumulative_sums[key] / counts[key] for key in cumulative_sums}
            for key in imageTags:
                imageTags[key] = avg_dict[key]
            frame_num += 10

        top_n = sorted(imageTags.items(), key=lambda item: item[1], reverse=True)[:3]
        top_n = dict(top_n)
        top_n = jsonify(top_n)
        
        return top_n
    else:
        return Response({"no": "no"}, status=201, mimetype='application/json')

@app.route('/frames/<filename>')
def get_frame(filename):
    return send_from_directory(app.config['FRAME_FOLDER'], filename)

def extract_frames(video_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
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
