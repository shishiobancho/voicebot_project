# VOICEVOX × ChatGPT 会話ボット

このプロジェクトは **VOICEVOX** を用いた音声合成と **OpenAI ChatGPT API** を組み合わせ、  
リアルタイムで会話できる音声ボットを構築するものです。  
OBS と連携して **字幕表示** にも対応しています。

---

## 機能一覧
- 🎙 **音声認識**（SpeechRecognition + PyAudio）
- 🤖 **ChatGPT 応答生成**（会話履歴付き）
- 🗣 **VOICEVOX による音声合成**
- 🔊 **pygame による音声再生**（ファイルロック解消済み）
- 👤 **キャラクター切り替え**（JSON定義 + エイリアス対応）
- 📝 **OBS への字幕出力**（HTML + JSONポーリング）
- 🎮 **VTube Studio 連携**（モデルロード・キャラ交代対応）

---

## 環境構築

```bash
# 必要なモジュールをインストール
pip install -r requirements.txt
```

### 必要モジュール
- openai
- python-dotenv
- requests
- pygame
- SpeechRecognition
- pyaudio
- websocket-client

---

## ディレクトリ構成

```
voicebot_project/
├─ run.bat                # 起動用スクリプト
├─ requirements.txt       # 必要なPythonモジュール
├─ README.md
├─ .gitignore
├─ config/
│   ├─ .env               # APIキーや設定値（Git管理外）
│   ├─ character_config.json   # キャラ定義 (ID, alias, color 等)
│   └─ stream_prompt/     # プロンプト管理
│        ├─ common.txt
│        ├─ ずんだもん.txt
│        └─ 春日部つむぎ.txt
├─ logs/                  # 実行ログ出力先
├─ audio/                 # 音声ファイル保存先
├─ src/
│   ├─ __init__.py
│   ├─ main.py            # エントリーポイント
│   ├─ utils.py           # 共通処理
│   ├─ core/
│   │    ├─ conversation.py   # GPT応答管理
│   │    └─ prompt_loader.py  # プロンプト読込
│   └─ voice/
│        ├─ recognition.py    # 音声認識
│        ├─ synthesis.py      # VOICEVOX音声合成
│        ├─ playback.py       # 音声再生
│        ├─ engine.py         # VOICEVOXエンジン管理
│        └─ subtitlemanager.py # 字幕出力管理
```

---

## VTube Studio 連携

- [VTube Studio](https://denchisoft.com/) をインストール  
- 設定 → プラグイン → WebSocket API を有効化  
- 初回起動時に API 認証キーを発行し、`config/.env` に追記  

例:
```env
VTS_AUTH_TOKEN=xxxxxxxx
```

キャラクターモデル名は `character_config.json` の `"modelName"` に一致させる必要があります。

---

## プロンプト管理

- 共通ルール: `config/stream_prompt/common.txt`  
- キャラ専用: `config/stream_prompt/<キャラ名>.txt`  

### キャラ追加手順
1. `character_config.json` にキャラ情報を追記（id, speed, alias, modelName, color）
2. `config/stream_prompt/<キャラ名>.txt` を作成して性格・配信スタイルを記述

---

## .gitignore

```
/config/.env
/audio/*.wav
/logs/*
__pycache__/
/*.pyc
```

---

## 実行方法

```bash
# Windows
run.bat
```

または

```bash
# Pythonモジュール実行
python -m src.main
```
