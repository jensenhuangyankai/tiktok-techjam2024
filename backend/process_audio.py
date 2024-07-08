import whisper
from transformers import pipeline
from pydub import AudioSegment
import os
import requests
import torch
# Load models
model = whisper.load_model("base")
device = "cuda" if torch.cuda.is_available() else "cpu"
classifier = pipeline(task="zero-shot-audio-classification", model="laion/clap-htsat-unfused", device=device)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn",device=device)


API_KEY = "c116b9cbea4c8ed588bf15747d9c466b"  # need update aft 20 july, free trial lasts 14 days :(

def convert_mp3_to_wav(mp3_file_path):
    wav_file_path = os.path.splitext(mp3_file_path)[0] + ".wav"
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")
    return wav_file_path

def classify_audio(audio_sample):
    candidate_labels = ['speech', 'music']
    probabilities = classifier(audio_sample, candidate_labels=candidate_labels)
    sorted_probabilities = sorted(probabilities, key=lambda x: x['score'], reverse=True)
    return sorted_probabilities[0]['label']

def transcribe_audio(file_path):
    audio_data = model.transcribe(file_path)
    return audio_data["text"]

def extract_keywords(text):
    summary = summarizer(text, max_length=10, min_length=1, do_sample=False)
    return summary[0]['summary_text']

def identify_song(file_path, api_key):
    url = 'https://api.audd.io/'
    data = {
        'api_token': api_key,
        'return': 'timecode,apple_music,spotify',
    }
    files = {
        'file': open(file_path, 'rb'),
    }
    response = requests.post(url, data=data, files=files)
    result = response.json()
    print(result['status'])
    if result['status'] == "success":
        return result["result"]["title"]
    else:
        return "failed to retrieve"

def trim_audio(audio_file_path, duration_ms=12000):
    try:
        audio = AudioSegment.from_wav(audio_file_path)
        trimmed_audio = audio[:duration_ms]
        trimmed_file_path = os.path.splitext(audio_file_path)[0] + "_trimmed.wav"
        trimmed_audio.export(trimmed_file_path, format="wav")
        return trimmed_file_path
    except Exception as e:
        print(f"Error trimming audio: {e}")
        return None

def process_audio(audio_file):
    if not audio_file:
        return []

    if audio_file.endswith('.mp3'):
        audio_file = convert_mp3_to_wav(audio_file)

    classification = classify_audio(audio_file)

    hashtags = []

    if classification == "speech":
        text = transcribe_audio(audio_file)
        text = text[:1000]
        print(f"text: {text}")

        if text:
            keywords = extract_keywords(text)
            print(f"keywords: {keywords}")
            keywords = keywords.split(" ")
            for word in keywords:
                hashtags.append(word)
        else:
            print("no keywords")
    else:
        print("music")
        title = ""
        if audio_file:
            try:
                trimmed_audio = trim_audio(audio_file)
                title = identify_song(trimmed_audio, API_KEY)
                title = "".join(char for char in title if char.isalnum())
                os.remove(trimmed_audio)
                hashtags.append(title)
            except Exception as e:
                title = f"failed to retrieve due to {str(e)}"
        print(f"Title: {title}")

    if audio_file.endswith('.wav'):
        os.remove(audio_file)

    print(hashtags)
    return hashtags

if __name__ == "__main__": #to remove, this is just fro testing
    audio_file_path = "backend/ted_test.mp3"  
    process_audio(audio_file_path)