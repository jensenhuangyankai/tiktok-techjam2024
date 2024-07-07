from flask import request, jsonify
import numpy as np
import os
from extract_features import extract_audio_features, extract_clip_features

def generate_hashtags():
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