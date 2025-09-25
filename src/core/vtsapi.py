# vtsapi.py
import websocket
import json
import os
import uuid
import time
import sys

class VTSAPI:
    def __init__(self, host="127.0.0.1", port=8001, token_file="config/authToken.json"):
        self.url = f"ws://{host}:{port}"
        self.ws = None
        self.token_file = token_file
        self.token = ""
        self.model_cache = {}  # {modelName: modelID}

        # 起動時にトークンを読み込み
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, "r", encoding="utf-8") as f:
                    self.token = json.load(f).get("authenticationToken", "")
            except Exception as e:
                print(f"[WARN] authToken.json 読み込み失敗: {e}")

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(self.url)

    def request_token(self, plugin_name="MyVoiceBot", developer="YourName"):
        """初回のみVTSから新しいトークンを取得"""
        req = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "token-1",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": plugin_name,
                "pluginDeveloper": developer
            }
        }
        self.ws.send(json.dumps(req))
        response = json.loads(self.ws.recv())

        token = response.get("data", {}).get("authenticationToken")
        if token:
            self.token = token
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, "w", encoding="utf-8") as f:
                json.dump({"authenticationToken": token}, f, ensure_ascii=False, indent=2)
            print("[INFO] 新しいトークンを保存しました")

        return response

    def authenticate(self, plugin_name="MyVoiceBot", developer="YourName"):
        """保存済みトークンで認証"""
        if not self.token:
            print("[ERROR] トークンがありません。先に request_token() を呼んでください。")
            return None

        request_id = f"auth-{uuid.uuid4().hex}"
        req = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": request_id,
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": plugin_name,
                "pluginDeveloper": developer,
                "authenticationToken": self.token
            }
        }
        self.ws.send(json.dumps(req))
        return json.loads(self.ws.recv())

    def get_models(self):
        """利用可能なモデル一覧を取得"""
        request_id = f"models-{uuid.uuid4().hex}"
        req = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": request_id,
            "messageType": "AvailableModelsRequest"
        }
        self.ws.send(json.dumps(req))
        return json.loads(self.ws.recv())

    def cache_models(self):
        """モデル一覧をキャッシュに保存 {modelName: modelID}"""
        response = self.get_models()
        models = response.get("data", {}).get("availableModels", [])
        for m in models:
            self.model_cache[m["modelName"]] = m["modelID"]
        print("[INFO] モデルキャッシュ:", self.model_cache)
        return self.model_cache

    def load_model(self, model_id, wait_response=True):
        request_id = f"load-{uuid.uuid4().hex}"
        print(f"[DEBUG] load_model request: model_id={model_id}, request_id={request_id}")

        req = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": request_id,
            "messageType": "ModelLoadRequest",
            "data": {"modelID": model_id}
        }
        try:
            self.ws.send(json.dumps(req))
        except Exception as e:
            print(f"[WARN] load_model send error: {e}")
            if self.reconnect():
                try:
                    self.ws.send(json.dumps(req))
                except Exception as e2:
                    print(f"[ERROR] retry send failed: {e2}")
                    return False

        if wait_response:
            # ここで明示的に長めのタイムアウトを設定（例: 10秒）
            self.ws.settimeout(12.0)
            try:
                while True:  # タイムアウトで例外が出るまでループ
                    resp_raw = self.ws.recv()
                    print(f"[DEBUG] raw response: {resp_raw}")
                    resp = json.loads(resp_raw)

                    # requestID が一致するレスポンスだけ採用
                    if resp.get("requestID") == request_id and resp.get("messageType") == "ModelLoadResponse":
                        return True
            except Exception as e:
                print(f"[WARN] recv timeout or error during load_model: {e}")
                return False

    def reconnect(self):
        try:
            self.close()    
            print("[INFO] Reconnecting to VTS...")

            self.connect()
            self.authenticate()
            self.cache_models()

            print("[INFO] Reconnected successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Reconnect failed: {e}")
            sys.exit(1)  # 再接続失敗したら終了

    def close(self):
        if self.ws:
            self.ws.close()
