import os
from src.utils import load_env # type: ignore

def load_prompt(character: str) -> str:
    """
    共通プロンプトとキャラ専用プロンプトを結合して返す
    - 共通プロンプト: .env の PROMPT_DIR + COMMON_PROMPT
    - キャラ専用: PROMPT_DIR/{キャラ名}.txt
    """
    env = load_env()
    prompt_dir = env["prompt_dir"]
    common_file = env["common_prompt"]

    # 共通プロンプト
    common_path = os.path.join(prompt_dir, common_file)
    common = ""
    if os.path.exists(common_path):
        with open(common_path, encoding="utf-8") as f:
            common = f.read()

    # キャラ専用プロンプト
    char_specific = ""
    char_file = f"{character}.txt"
    char_path = os.path.join(prompt_dir, char_file)
    if os.path.exists(char_path):
        with open(char_path, encoding="utf-8") as f:
            char_specific = f.read()

    return common + "\n" + char_specific
