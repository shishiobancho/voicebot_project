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
    get_character_by_alias,
    should_change_character,
    detect_character,
    character_config
)
from subtitlemanager import save_user_subtitle, save_character_subtitle, start_clear_timer

# 初期化
load_dotenv()
DEFAULT_CHARACTER = get_default_character()
current_character = DEFAULT_CHARACTER

# VOICEVOXエンジンの起動
start_voicevox_engine(
    os.getenv("VOICEVOX_ENGINE_PATH"),
    os.getenv("VOICEVOX_URL")
)

# 終了ワード
EXIT_WORDS = ["終了", "終わり", "おしまい", "バイバイ", "さよなら"]

# メインループ
while True:
    print("========== 新しいループ ==========")
    print("話してください...")

    user_input = recognize_speech()
    if not user_input:
        continue

    print(f"{os.getenv('USER_NAME', 'あなた')}: {user_input}")
    save_user_subtitle(user_input)

    # キャラ切り替え判定
    alias = detect_character(user_input)
    if should_change_character(user_input, alias) and alias != current_character:
        current_character = alias
        print(f"[DEBUG] キャラを「{current_character}」に変更しました")

    # 応答生成
    character_info = get_character_info(current_character)
    reply_text = chat_with_gpt(user_input, current_character, character_info)
    print(f"{current_character}: {reply_text}")
    save_character_subtitle(current_character, reply_text, character_info)

    # 音声合成・再生
    speaker_id = character_info.get("id")
    speed = character_info.get("speed", 1.0)
    wav_path = synthesize_speech(reply_text, speaker_id, speed)

    if wav_path:
        play_audio(wav_path)
        # 再生完了後に字幕クリアのタイマー開始
        start_clear_timer()
    else:
        print("[エラー] 音声ファイルが生成されませんでした")

    # 終了判定（応答後に終了）
    if any(word in user_input for word in EXIT_WORDS):
        break
