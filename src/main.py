from dotenv import load_dotenv
import os

from src.voice.engine import start_voicevox_engine
from src.voice.recognition import recognize_speech
from src.voice.synthesis import synthesize_speech
from src.voice.playback import play_audio
from src.core.conversation import chat_with_gpt
from src.core.character import ( # pyright: ignore[reportMissingImports]
    get_default_character,
    get_character_info,
    should_change_character,
    detect_character
)
from src.subtitlemanager import save_user_subtitle, save_character_subtitle
from src.core.vtsapi import VTSAPI
from src.core.character import get_character_id_by_name  # 仮の関数、キャラ名→modelID対応
from src.utils import split_text_simple, load_env
from src.core.prompt_loader import load_prompt

# 終了ワード
EXIT_WORDS = ["終了", "終わり", "おしまい", "バイバイ", "さよなら"]

# 初期化
env = load_env()
DEFAULT_CHARACTER = get_default_character()
current_character = DEFAULT_CHARACTER
MAX_CHARS = env["max_chars"]


# VOICEVOXエンジンの起動
start_voicevox_engine(
    os.getenv("VOICEVOX_ENGINE_PATH"),
    os.getenv("VOICEVOX_URL")
)

# VTS初期化
vts = VTSAPI()
vts.connect()
if not vts.token:
    print("[INFO] トークン未保存 → 新規発行します")
    vts.request_token()
auth_response = vts.authenticate()
if not auth_response or not auth_response.get("data", {}).get("authenticated", False):
    raise RuntimeError(f"VTS認証失敗: {auth_response}")
print("[INFO] VTS認証に成功しました")
# 起動時にキャッシュ作成
vts.get_models()
vts.cache_models()
# デフォルトキャラクター設定
model_id = get_character_id_by_name(current_character, vts.model_cache)
vts.load_model(model_id, wait_response=False)

first_turn = True

# メインループ
while True:
    print("-----発話待機中-----")

    user_input = recognize_speech()
    if not user_input:
        continue

    print(f"{os.getenv('USER_NAME', 'あなた')}: {user_input}")
    save_user_subtitle(user_input)

    # キャラ切り替え
    alias = detect_character(user_input)
    if should_change_character(user_input, alias) and alias != current_character:
        model_id = get_character_id_by_name(alias, vts.model_cache)
        if model_id:
            success = vts.load_model(model_id, wait_response=True)
            if success:
                current_character = alias
                print(f"[DEBUG] キャラを「{current_character}」に変更しました")
            else:
                print(f"[WARN] キャラ「{alias}」の切り替えに失敗しました")
                user_input = f"キャラクター交代に失敗したので、{current_character}は忙しいとユーザーに伝えて"

    # 応答生成
    character_info = get_character_info(current_character)
    reply_text = chat_with_gpt(user_input, current_character)

    print(f"{current_character}: {reply_text}")

    # 区切り処理（最大文字数ベース）
    segments = split_text_simple(reply_text, max_chars=MAX_CHARS)

    for seg in segments:
        # 字幕表示
        save_character_subtitle(seg, character_info.get("color", "white"))

        # 音声合成
        speaker_id = character_info.get("id")
        speed = character_info.get("speed", 1.0)
        wav_path = synthesize_speech(seg, speaker_id, speed)

        if wav_path:
            play_audio(wav_path)
        else:
            print("[エラー] 音声ファイルが生成されませんでした")

    # 終了判定（応答後に終了）
    if any(word in user_input for word in EXIT_WORDS):
        break
