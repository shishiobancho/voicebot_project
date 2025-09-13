# src/voice/engine.py
import requests
import psutil
import subprocess
import time
import os

def is_voicevox_running(voicevox_url):
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['exe'] and "run.exe" in proc.info['exe']:
                try:
                    response = requests.get(voicevox_url)
                    if response.status_code == 200:
                        return True
                except:
                    pass
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def start_voicevox_engine(engine_path, voicevox_url):
    if is_voicevox_running(voicevox_url):
        print("[DEBUG] VOICEVOXエンジンはすでに起動中です")
        return
    try:
        subprocess.Popen(engine_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[DEBUG] VOICEVOXエンジンを起動しました")
        time.sleep(3)
    except Exception as e:
        print(f"[致命的エラー] VOICEVOXエンジンの起動に失敗しました: {e}")
