# 多分キッカー用プログラムになる

import requests, yaml # ライブラリのインポート requestsはAPIを叩くためのライブラリ、yamlは設定ファイルを読み込むためのライブラリ

url ="https://public.api.aibo.com" # aiboのAPIのURL
with open("config.yaml") as f: # config.yamlを読み込む
    token = yaml.load(f, Loader=yaml.SafeLoader)["token"] # config.yamlのtokenを取得

headers = {"Authorization": f"Bearer {token}",} # ヘッダーの設定 AuthorizationにBearer +APIトークンを設定
deviceId = requests.get(url+"/v1/devices", headers=headers).json()["devices"][0]["deviceId"] # デバイスIDを取得 今回は一つのデバイスのみを想定

resp= requests.post(url+f"/v1/devices/{deviceId}/capabilities/set_mode/execute", headers=headers, json={"arguments":{"ModeName":"DEVELOPMENT"}}) # 指示待ちモードに設定