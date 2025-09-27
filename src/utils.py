import os
import json
from dotenv import load_dotenv

def load_env():
    # プロジェクトルート/config/.env を明示的に指定
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "config", ".env")
    load_dotenv(dotenv_path)

    return {
        "voicevox_url": os.getenv("VOICEVOX_URL"),
        "voicevox_engine_path": os.getenv("VOICEVOX_ENGINE_PATH"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "max_chars": int(os.getenv("MAX_CHARS", 20)),
        "prompt_dir": os.getenv("PROMPT_DIR", "config/stream_prompt"),
        "common_prompt": os.getenv("COMMON_PROMPT", "common.txt"),
    }

def load_keywords(key: str) -> list[str]:
    words = os.getenv(key, "")
    return [w.strip() for w in words.split(",") if w.strip()]

def load_character_config(path="./config/character_config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def split_text_simple(text, max_chars=60):
    """
    最大文字数を超えないようにテキストを分割する。
    - max_charsを超えたら直前の「。」で区切り
    - 「。」が無い場合は強制的にmax_charsで区切り
    """
    segments = []
    start = 0

    while start < len(text):
        # 今回の区切り候補
        end = start + max_chars
        if end >= len(text):
            segments.append(text[start:])
            break

        # max_chars以内で最後に出た「。」を探す
        last_period = text.rfind("。", start, end)
        if last_period != -1:
            end = last_period + 1  # 「。」も含めて切る
        segments.append(text[start:end])
        start = end

    return segments



