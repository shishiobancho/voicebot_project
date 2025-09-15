import os
import json
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return {
        "voicevox_url": os.getenv("VOICEVOX_URL"),
        "voicevox_engine_path": os.getenv("VOICEVOX_ENGINE_PATH"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
    }

def load_character_config(path="./config/character_config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

