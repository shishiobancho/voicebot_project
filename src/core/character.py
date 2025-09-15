import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# 設定ファイルのパス
CHARACTER_CONFIG_PATH = os.path.join("config", "character_config.json")

CHANGE_WORDS = ["代わって", "変わって", "と交代して"]

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


def detect_character(text: str):
    """入力テキスト中からキャラクター名またはaliasを検出"""
    normalized = text.replace(" ", "").replace("　", "")  # 半角・全角スペースを削除
    for name, data in character_config.items():
        # 正式名チェック
        if name.replace(" ", "").replace("　", "") in normalized:
            return name
        # エイリアスチェック（スペース無視）
        for alias in data.get("aliases", []):
            alias_normalized = alias.replace(" ", "").replace("　", "")
            if alias_normalized in normalized:
                return name
    return None


def should_change_character(user_input: str, detected_character: str) -> bool:
    """交代ワードが含まれていて、かつキャラが検出されていれば True"""
    if not detected_character:
        return False

    change_words = ["代わって", "変わって", "交代して"]

    return any(word in user_input for word in change_words)

