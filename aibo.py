import requests, yaml # ライブラリのインポート requestsはAPIを叩くためのライブラリ、yamlは設定ファイルを読み込むためのライブラリ

url ="https://public.api.aibo.com" # aiboのAPIのURL
with open("config.yaml") as f: # config.yamlを読み込む
    token = yaml.load(f, Loader=yaml.SafeLoader)["token"] # config.yamlのtokenを取得

headers = {"Authorization": f"Bearer {token}",} # ヘッダーの設定 AuthorizationにBearer +APIトークンを設定

def POST(urlSuf,json): # POSTリクエストを送る関数 urlSufはURLの後ろに追加する文字列、jsonは送信するjson
    resp= requests.post(url+urlSuf, headers=headers, json=json) # POSTリクエストを送信
    if resp.status_code != 200: # ステータスコードが200以外の時
        raise Exception(f"Status code {resp.status_code}") # 例外を出力
    return resp # レスポンスを返す

def GET(urlSuf): # GETリクエストを送る関数 urlSufはURLの後ろに追加する文字列
    resp= requests.get(url+urlSuf, headers=headers) # GETリクエストを送信
    if resp.status_code != 200: # ステータスコードが200以外の時
        raise Exception(f"Status code {resp.status_code}") # 例外を出力
    return resp # レスポンスを返す


deviceId = GET("/v1/devices").json()["devices"][0]["deviceId"] # デバイスIDを取得 今回は一つのデバイスのみを想定




resp = POST(f"/v1/devices/{deviceId}/capabilities/set_mode/execute", {"arguments":{"ModeName":"DEVELOPMENT"}}) # 指示待ちモードに設定
print(f"[{resp.json()["status"]}] SetMode:DEVELOPMENT")