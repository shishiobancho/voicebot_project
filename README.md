# VOICEVOX × ChatGPT 会話ボット

このプロジェクトは **VOICEVOX** を用いた音声合成と **OpenAI ChatGPT API** を組み合わせ、  
リアルタイムで会話できる音声ボットを構築するものです。  
OBS と連携して **字幕表示** にも対応しています。

---

## 機能一覧
- 🎙 音声認識（SpeechRecognition + PyAudio）
- 🤖 ChatGPT 応答生成（会話履歴付き）
- 🗣 VOICEVOX による音声合成
- 🔊 pygame による音声再生（ファイルロック解消済み）
- 👤 キャラクター切り替え（JSON定義 + エイリアス対応）
- 📝 OBS への字幕出力（HTML + JSONポーリング）

---

## ディレクトリ構成
```
voicebot_project/
├── config/
│   ├── .env                  # APIキーやデフォルトキャラ設定
│   └── character_config.json # キャラごとのID・話速・色など
├── src/
│   ├── core/
│   │   ├── character.py      # キャラ管理
│   │   └── conversation.py   # ChatGPT応答処理
│   ├── voice/
│   │   ├── engine.py         # VOICEVOXエンジン起動管理
│   │   ├── recognition.py    # 音声認識
│   │   ├── synthesis.py      # 音声合成
│   │   └── playback.py       # 音声再生
│   ├── subtitlemanager.py    # OBS字幕制御
│   ├── utils.py              # 共通処理（env読込など）
│   └── main.py               # エントリーポイント
├── subtitles/
│   ├── index.html            # OBS用字幕表示
│   ├── subtitle.css          # 字幕スタイル
│   └── subtitle.json         # 字幕データ（プログラムが更新）
├── requirements.txt
├── run.bat
└── README.md
```

---

## セットアップ

### 1. 環境準備
- Python 3.12 以上を推奨
- 必要ライブラリをインストール
  ```bash
  pip install -r requirements.txt
  ```

### 2. VOICEVOX エンジン
- [VOICEVOXエンジン](https://github.com/VOICEVOX/voicevox_engine) をダウンロード
- `config/.env` にパスを記載
  ```env
  VOICEVOX_ENGINE_PATH=C:\voicebox_engine\windows-cpu\voicevox-engine\run.exe
  VOICEVOX_URL=http://127.0.0.1:50021
  ```

### 3. OpenAI API
- [OpenAI](https://platform.openai.com/) で APIキーを取得
- `config/.env` に記載
  ```env
  OPENAI_API_KEY=sk-xxxx
  OPENAI_MODEL=gpt-4o
  ```

### 4. 実行
```bash
python -m src.main
```

---

## OBS 連携（字幕表示）

### 設定手順
1. OBS → **ソース → ブラウザ** を追加
2. 「ローカルファイルを使用」にチェックを入れ、以下を指定
   ```
   <プロジェクトルート>/subtitles/index.html
   ```
3. 推奨設定
   - 幅: 1920（配信解像度に合わせる）
   - 高さ: 200〜300
   - 背景色: 透明
4. 字幕スタイルは `subtitles/subtitle.css` を編集

### 字幕の仕様
- **ユーザー発話** → `cyan`（水色）
- **キャラクター発話** → キャラごとに `character_config.json` で色を定義
- **クリア処理**  
  - ユーザーが発話 → 字幕をリセットして新規表示  
  - キャラが応答 → ユーザー行を残したままキャラ行を追加  
  - 一定時間（デフォルト8秒）発話がなければ字幕をクリア  

---

## 今後の課題
- ⏱ 会話テンポの改善（応答までの待ち時間短縮）
- 📜 キャラごとのシステムプロンプト外部管理
- 🎥 OBS連携機能拡張（立ち絵切替など）

---

## ライセンス
このプロジェクトは学習・配信用途を想定しています。  
VOICEVOXのキャラクターボイス利用にあたっては、各キャラクターの利用規約に従ってください。
