from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import clip
import torch
from PIL import Image
import numpy as np
import joblib
import os
import librosa

app = Flask(__name__)
CORS(app)

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load your trained logistic regression model
logistic_model = joblib.load('trained_model.pkl')  # Ensure you save and load your model properly

# Load your MultiLabelBinarizer
mlb = joblib.load('mlb.pkl')  # Ensure you save and load your binarizer properly

def extract_frames(video_path, frame_rate=1):
    video_capture = cv2.VideoCapture(video_path)
    frames = []
    success, frame = video_capture.read()
    count = 0
    while success:
        if count % frame_rate == 0:
            frames.append(frame)
        success, frame = video_capture.read()
        count += 1
    video_capture.release()
    return frames

def extract_clip_features(frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
    return image_features.cpu().numpy()

def extract_audio_features(video_path):
    y, sr = librosa.load(video_path, sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

@app.route("/generate_hashtags/", methods=["POST"])
def generate_hashtags():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        video_path = os.path.join("temp_videos", file.filename)
        os.makedirs("temp_videos", exist_ok=True)
        file.save(video_path)

        frames = extract_frames(video_path)
        frame_features = extract_clip_features(frames)
        averaged_frame_features = np.mean(frame_features, axis=0)

        audio_features = extract_audio_features(video_path)

        combined_features = np.concatenate((averaged_frame_features, audio_features)).reshape(1, -1)

        hashtags = logistic_model.predict(combined_features)
        predicted_hashtags = mlb.inverse_transform(hashtags)[0]

        print(predicted_hashtags)
        return jsonify({"hashtags": predicted_hashtags})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)