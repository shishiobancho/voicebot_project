import os
import json
from dotenv import load_dotenv

load_dotenv()

# 設定ファイルのパス
CHARACTER_CONFIG_PATH = os.path.join("config", "character_config.json")


# キャラ設定ファイルを読み込む
def load_character_config():
    with open(CHARACTER_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# グローバルに1回だけ読み込んでキャッシュ
character_config = load_character_config()


# .envで指定されたデフォルトキャラを返す（なければ春日部つむぎ）
def get_default_character():
    return os.getenv("DEFAULT_CHARACTER", "春日部つむぎ")


# 別名（alias）から正式キャラ名を返す（なければNone）
def get_character_by_alias(alias: str):
    for name, data in character_config.items():
        if alias == name or alias in data.get("aliases", []):
            return name
    return None


# キャラ名に対応する詳細情報（speaker_idやスタイルなど）を返す
def get_character_info(name: str):
    return character_config.get(name)


# 入力テキスト中からキャラクター名またはaliasを検出して正式名を返す
def detect_character(text: str):
    for name, data in character_config.items():
        # 正式名が含まれていたら返す
        if name in text:
            return name
        # エイリアスが含まれていたら返す
        for alias in data.get("aliases", []):
            if alias in text:
                return name
    return None
