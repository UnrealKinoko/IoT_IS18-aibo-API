# 2024 前期IoT授業 IS18-1-7
# 多分キッカー用プログラムになる
# チームメンバーへ コメントたくさんつけるので頑張って読んで❤
# コメントは基本copilotに任せてる
# 授業中以外に動かすとAiboが夜中に暴れたりする可能性があるため注意

import requests, yaml # ライブラリのインポート requestsはAPIを叩くためのライブラリ、yamlは設定ファイルを読み込むためのライブラリ

url ="https://public.api.aibo.com" # aiboのAPIのURL
with open("config.yaml") as f: # config.yamlを読み込む
    token = yaml.load(f, Loader=yaml.SafeLoader)["token"] # config.yamlのtokenを取得

headers = {"Authorization": f"Bearer {token}",} # ヘッダーの設定 AuthorizationにBearer +APIトークンを設定
deviceId = requests.get(url+"/v1/devices", headers=headers).json()["devices"][0]["deviceId"] # デバイスIDを取得 今回は一つのデバイスのみを想定

resp= requests.post(url+f"/v1/devices/{deviceId}/capabilities/set_mode/execute", headers=headers, json={"arguments":{"ModeName":"DEVELOPMENT"}}) # 指示待ちモードに設定