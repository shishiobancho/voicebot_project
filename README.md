# VOICEBOT Project

VOICEVOX × ChatGPT を組み合わせた音声会話ボットです。  
マイクから音声を入力し、ChatGPTで返答を生成し、VOICEVOXで合成音声を再生します。

---

## 必要環境
- Python 3.12
- VOICEVOX エンジン（ローカルで起動）
- マイク入力環境
- Git

---

## セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/shishiobancho/voicebot_project.git
cd voicebot_project

# パッケージをインストール
pip install -r requirements.txt
```

次に `config/.env` を作成して以下を記入してください。

```env
OPENAI_API_KEY=sk-xxxx...
VOICEVOX_ENGINE_PATH=C:\voicebox_engine\windows-cpu\run.exe
VOICEVOX_URL=http://127.0.0.1:50021
DEFAULT_CHARACTER=ずんだもん
```

---

## 実行方法

Windows の場合:

```bash
run.bat
```

または:

```bash
python -m src.main
```

---

## 注意事項
- `.env` や音声ファイルは `.gitignore` 済みなので GitHub にはアップロードされません。
- 終了する場合は音声入力で「終了」「バイバイ」などのキーワードを話してください。
