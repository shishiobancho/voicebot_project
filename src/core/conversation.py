import os
import json
from openai import OpenAI
from src.utils import load_env # type: ignore
from src.core.prompt_loader import load_prompt  # type: ignore # ← 今回作る load_prompt をここから呼ぶ想定

# 環境変数読み込み
env = load_env()
api_key = env.get("openai_api_key")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY が読み込めませんでした")

client = OpenAI(api_key=api_key)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

# 会話履歴管理
MAX_HISTORY = 5  # 5往復ぶん保持
conversation_history = []

def append_message(role, content):
    """
    会話履歴に追加し、最大長を超えたら古いものを削除
    """
    global conversation_history
    conversation_history.append({"role": role, "content": content})
    if len(conversation_history) > MAX_HISTORY * 2:
        conversation_history = conversation_history[-MAX_HISTORY * 2:]


def chat_with_gpt(user_input, character_name):
    """
    ChatGPT に問い合わせて応答を返す
    - user_input: ユーザー発話
    - character_name: 現在のキャラ名
    - character_info: キャラ設定情報（character_config.jsonから）
    """
    # 共通＋キャラ専用プロンプトをロード
    system_prompt = load_prompt(character_name)
    system_prompt_msg = {"role": "system", "content": system_prompt}

    # 履歴に追加
    append_message("user", user_input)
    messages = [system_prompt_msg] + conversation_history

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
        append_message("assistant", reply)
        return reply
    except Exception as e:
        return f"[エラー] ChatGPT API呼び出しに失敗しました: {e}"
