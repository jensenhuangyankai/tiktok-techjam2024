import json
import os
import cv2
import clip
import torch
from PIL import Image
import numpy as np
import librosa
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

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

def extract_clip_features(frames):
    frame_features = []
    for frame in frames:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            image_features = model.encode_image(image)
        frame_features.append(image_features.cpu().numpy())
    return np.array(frame_features)

def extract_audio_features(video_path):
    y, sr = librosa.load(video_path, sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

data_dir = "data"
features = []
labels = []

for hashtag in ["london", "paris", "newyork"]:
    posts_file = os.path.join(data_dir, hashtag, "posts.json")
    with open(posts_file, "r") as f:
        posts = json.load(f)

    for post in posts:
        video_path = os.path.join(data_dir, hashtag, "media", post["video_id"] + ".mp4")
        frames = extract_frames(video_path)
        frame_features = extract_clip_features(frames)
        averaged_frame_features = np.mean(frame_features, axis=0)

        audio_features = extract_audio_features(video_path)

        combined_features = np.concatenate((averaged_frame_features, audio_features))

        features.append(combined_features)
        labels.append(post["hashtags"])

features = np.array(features)
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(labels)

# Save the features and labels for future use
np.save('features.npy', features)
np.save('labels.npy', y)
joblib.dump(mlb, 'mlb.pkl')
