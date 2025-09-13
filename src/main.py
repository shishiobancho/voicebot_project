from dotenv import load_dotenv
import os

from voice.engine import start_voicevox_engine
from voice.recognition import recognize_speech
from voice.synthesis import synthesize_speech
from voice.playback import play_audio
from core.conversation import chat_with_gpt
from core.character import (
    get_default_character,
    get_character_info,
    get_character_by_alias
)

# 初期化
load_dotenv()
DEFAULT_CHARACTER = get_default_character()
current_character = DEFAULT_CHARACTER

# VOICEVOXエンジンの起動
start_voicevox_engine(
    os.getenv("VOICEVOX_ENGINE_PATH"),
    os.getenv("VOICEVOX_URL")
)

# メインループ
while True:
    print("========== 新しいループ ==========")
    print("話してください...")

    user_input = recognize_speech()
    if not user_input:
        continue

    print(f"{os.getenv('USER_NAME', 'あなた')}: {user_input}")

    if user_input in ["終了", "exit", "quit", "おしまい", "バイバイ"]:
        # GPTに終了メッセージを生成させる
        farewell_text = chat_with_gpt(
            "終了の挨拶を一言お願いします。",
            current_character,
            get_character_info(current_character)
        )
        print(f"{current_character}: {farewell_text}")

        wav_path = synthesize_speech(
            text=farewell_text,
            speaker_id=get_character_info(current_character)["id"],
            speed=get_character_info(current_character)["speed"]
        )
        if wav_path:
            play_audio(wav_path)

        break

    # キャラ切り替え判定
    alias = get_character_by_alias(user_input)
    if alias and alias != current_character:
        current_character = alias
        print(f"[DEBUG] キャラを「{current_character}」に変更しました")
        continue

    # 応答生成
    reply_text = chat_with_gpt(user_input, current_character, get_character_info(current_character))
    print(f"{current_character}: {reply_text}")

    # 音声合成・再生
    character_info = get_character_info(current_character)
    wav_path = synthesize_speech(
        text=reply_text,
        speaker_id=character_info["id"],      # ← IDを渡す
        speed=character_info["speed"]          # ← 話速も反映
            ) 
    play_audio(wav_path)
