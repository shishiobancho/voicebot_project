import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

VOICEVOX_URL = os.getenv("VOICEVOX_URL", "http://127.0.0.1:50021")

def synthesize_speech(text: str, speaker_id: int, speed: float = 1.0) -> str:
    """
    VOICEVOXエンジンを使って音声を合成し、再生用WAVファイルとして保存する。
    :param text: 合成する文章
    :param speaker_id: VOICEVOXのキャラID
    :param speed: 話速（1.0 = 通常）
    :return: 成功すれば保存先ファイルパス、失敗すればNONE
    """

    try:
        # 音声ファイル保存先
        filename = "audio/output.wav"

        # AudioQuery の作成
        query_payload = {
            "text": text,
            "speaker": speaker_id
        }
        query_response = requests.post(
            f"{VOICEVOX_URL}/audio_query",
            params=query_payload
        )
        query_response.raise_for_status()

        query = query_response.json()
        query["speedScale"] = speed  # 話速を設定

        # 音声合成（synthesis）
        synth_response = requests.post(
            f"{VOICEVOX_URL}/synthesis",
            params={"speaker": speaker_id},
            headers={"Content-Type": "application/json"},
            data=json.dumps(query)
        )
        query_response.raise_for_status()

        # WAVファイルとして保存
        with open(filename, "wb") as f:
            f.write(synth_response.content)

        return filename  # ← 成功時はパスを返す

    except Exception as e:
        print(f"[致命的エラー] 音声合成中に例外が発生: {e}")
        return None
