import os
import json
import threading

SUBTITLE_JSON = os.path.join("subtitles", "subtitle.json")

_clear_timer = None
_clear_delay = 8  # 秒
_current_user = None
_current_character = None

def _write_json():
    """現在の字幕状態をJSONに保存"""
    os.makedirs(os.path.dirname(SUBTITLE_JSON), exist_ok=True)
    data = {
        "user": _current_user,
        "character": _current_character
    }
    with open(SUBTITLE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def save_user_subtitle(text: str):
    """ユーザー発話時：字幕をリセットしてユーザー行のみ表示"""
    global _current_user, _current_character
    _cancel_timer()
    _current_user = f"<span class='user'>{text}</span>"
    _current_character = None  # キャラ行を消す
    _write_json()

def save_character_subtitle(character: str, text: str, color: str = "white"):
    """キャラ発話時：キャラ行を追加、ユーザー行は残す"""
    global _current_character
    _current_character = f"<span style='color:{color}'>{character}: {text}</span>"
    _write_json()

def _start_timer():
    global _clear_timer
    _cancel_timer()
    _clear_timer = threading.Timer(_clear_delay, clear_subtitles)
    _clear_timer.start()

def _cancel_timer():
    global _clear_timer
    if _clear_timer:
        _clear_timer.cancel()
        _clear_timer = None

def clear_subtitles():
    """両方クリア"""
    global _current_user, _current_character
    _current_user, _current_character = None, None
    _write_json()

def start_clear_timer():
    """外部から呼び出せるタイマー開始"""
    _start_timer()
