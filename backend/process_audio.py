import whisper
from transformers import pipeline
from extract_features import extract_audio_features
from pydub import AudioSegment
import os
import requests

API_KEY = "https://api.audd.io/"
model = whisper.load_model("base")

def process_audio(audio_file):

    def convert_mp3_to_wav(mp3_file_path):
        wav_file_path = os.path.splitext(mp3_file_path)[0] + ".wav"
        audio = AudioSegment.from_mp3(mp3_file_path)
        audio.export(wav_file_path, format="wav")
        return wav_file_path

    def classify_audio(audio_sample):
        candidate_labels = ['speech', 'music']
        classifier = pipeline(
                        task="zero-shot-audio-classification", model="laion/clap-htsat-unfused"
                    )
        probabilities = classifier(audio_sample, candidate_labels=candidate_labels)
        
        sorted_probabilities = sorted(probabilities, key=lambda x: x['score'], reverse=True)

        return sorted_probabilities[0]['label']
    
    def transcribe_audio(file_path):
    
        audio_data = model.transcribe(file_path)

        return audio_data["text"]

    def extract_keywords(text):
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
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
        return result["result"]["title"]

    if audio_file.endswith('.mp3'):
        audio_file = convert_mp3_to_wav(audio_file)

    classification=classify_audio(audio_file)

    if classification == "speech":
        text = transcribe_audio(audio_file)
        text = text[:1000]
        print(f"text: {text}")

        if text:
            keywords = extract_keywords(text)
            print(f"keywords: {keywords}")
        else:
            print("no keywords")
    else:
        print(f"music")
        title = ""
        if audio_file:
            try:
                title = identify_song(audio_file, API_KEY)
            except:
                title = "failed to retrieve"
        print(f"Title: {title}")
                

    if audio_file:
        os.remove(audio_file)

    hashtags = ""
    return hashtags

if __name__ == "__main__":
    audio_file_path = "backend/ted_test.mp3"  # Update this to your actual audio file path
    process_audio(audio_file_path)