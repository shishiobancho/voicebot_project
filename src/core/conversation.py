import os
from openai import OpenAI
from dotenv import load_dotenv

#load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# config/.env を明示的にロード
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", "config", ".env"))

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY が読み込めませんでした")

client = OpenAI(api_key=api_key)  # ← これ必須



OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# 履歴保存（最大5往復＝10件）
MAX_HISTORY = 5
conversation_history = []

# キャラプロンプトを付加
def build_prompt(character_name, character_info):
    style = character_info.get("prompt", "")
    return {
        "role": "system",
        "content": f"{character_name}として振る舞ってください。{style}"
    }

# 会話履歴に追加（古い履歴は削除）
def append_message(role, content):
    global conversation_history
    conversation_history.append({"role": role, "content": content})
    if len(conversation_history) > MAX_HISTORY * 2:
        conversation_history = conversation_history[-MAX_HISTORY * 2:]

# GPTと対話
def chat_with_gpt(user_input, character_name, character_info):
    system_prompt = build_prompt(character_name, character_info)

    # 履歴にユーザー発話を追加
    append_message("user", user_input)

    # OpenAIに投げるメッセージ構成
    messages = [system_prompt] + conversation_history

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        # アシスタントの返答も履歴に追加
        append_message("assistant", reply)
        return reply
    except Exception as e:
        return f"[エラー] ChatGPT API呼び出しに失敗しました: {e}"
