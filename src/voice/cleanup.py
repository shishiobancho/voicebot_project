# src/voice/cleanup.py

import os
import threading
import time
from dotenv import load_dotenv

load_dotenv()

MAX_FILES = int(os.getenv("MAX_AUDIO_FILES", 50))
DELETE_COUNT = int(os.getenv("DELETE_AUDIO_COUNT", 10))
AUDIO_DIR = os.getenv("AUDIO_OUTPUT_DIR", "audio/logs")

def cleanup_old_audio_files():
    def _cleanup():
        try:
            files = [
                os.path.join(AUDIO_DIR, f)
                for f in os.listdir(AUDIO_DIR)
                if f.endswith(".wav")
            ]
            files.sort(key=lambda x: os.path.getctime(x))  # 古い順にソート

            if len(files) > MAX_FILES:
                for file_path in files[:DELETE_COUNT]:
                    try:
                        os.remove(file_path)
                        print(f"[DEBUG] 削除: {file_path}")
                    except Exception as e:
                        print(f"[エラー] 削除失敗: {file_path} -> {e}")
        except Exception as e:
            print(f"[致命的エラー] クリーンアップ処理に失敗: {e}")

    # 並列スレッドで処理（非同期にする）
    thread = threading.Thread(target=_cleanup)
    thread.start()
