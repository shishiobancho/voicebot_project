# src/voice/recognition.py

import speech_recognition as sr
import os
from dotenv import load_dotenv

load_dotenv()
SPEAKER_DISPLAY_NAME = os.getenv("SPEAKER_DISPLAY_NAME", "あなた")

recognizer = sr.Recognizer()
mic = sr.Microphone()

def recognize_speech():
    with mic as source:
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        return text
    except sr.UnknownValueError:
        print("[エラー] 音声を認識できませんでした")
    except sr.RequestError:
        print("[エラー] Google音声認識サービスに接続できませんでした")
    return ""
