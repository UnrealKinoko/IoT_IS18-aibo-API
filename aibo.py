import requests, yaml, time # ライブラリのインポート requestsはAPIを叩くためのライブラリ、yamlは設定ファイルを読み込むためのライブラリ

url ="https://public.api.aibo.com" # aiboのAPIのURL
with open("config.yaml") as f: # config.yamlを読み込む
    token = yaml.load(f, Loader=yaml.SafeLoader)["kicker"]["token"] # config.yamlのtokenを取得
    print("token loaded")

headers = {"Authorization": f"Bearer {token}",} # ヘッダーの設定 AuthorizationにBearer +APIトークンを設定

def statCodeBranch(urlSuf,resp):
    match resp.status_code:
        case 400:
            raise Exception(f"{urlSuf} 400:Bad Request ボディを確認してください")
        case 401:
            raise Exception(f"{urlSuf} 401:Unauthorized トークンを確認してください")
        case 403:
            raise Exception(f"{urlSuf} 403:Forbidden 権限を確認してください")
        case 404:
            raise Exception(f"{urlSuf} 404:Not Found URLを確認してください")
        case 429:
            raise Exception(f"{urlSuf} 429:Too Many Requests APIレート制限を超過しました")
        case 500:
            raise Exception(f"{urlSuf} 500:Internal Server Error サーバー側のエラーです")
        case 503:
            raise Exception(f"{urlSuf} 503:Service Unavailable サービスが利用できません")

def POST(urlSuf,json): # POSTリクエストを送る関数 urlSufはURLの後ろに追加する文字列、jsonは送信するjson
    for i in range(3):
        print(f"POST:{url}{urlSuf} >> ",end="")
        resp= requests.post(url+urlSuf, headers=headers, json=json) # POSTリクエストを送信
        if resp.status_code == 200:
            print("OK")
            break
        elif i == 2 and resp.status_code != 200:
            print(f"Failed {resp.status_code}")
            statCodeBranch(urlSuf,resp)
        else:
            print(f"Failed {resp.status_code}")
        time.sleep(3)
    return resp # レスポンスを返す

def GET(urlSuf): # GETリクエストを送る関数 urlSufはURLの後ろに追加する文字列
    for i in range(3):
        print(f"GET:{url}{urlSuf} >> ",end="")
        resp= requests.get(url+urlSuf, headers=headers) # GETリクエストを送信
        if resp.status_code == 200:
            print("OK")
            break
        elif i == 2 and resp.status_code != 200:
            print(f"Failed {resp.status_code}")
            statCodeBranch(urlSuf,resp)
        else:
            print(f"Failed {resp.status_code}")
        time.sleep(3)
    return resp # レスポンスを返す

deviceId = GET("/v1/devices").json()["devices"][0]["deviceId"] # デバイスIDを取得 今回は一つのデバイスのみを想定

resp = POST(f"/v1/devices/{deviceId}/capabilities/set_mode/execute", {"arguments":{"ModeName":"DEVELOPMENT"}}) # 指示待ちモードに設定
while GET(f"/v1/executions/{resp.json()["executionId"]}").json()["status"] != "SUCCEEDED": # 完了するまで待機
    print(GET(f"/v1/executions/{resp.json()["executionId"]}").json()["status"])
    time.sleep(5)
    # resp = GET(f"/v1/devices/{deviceId}/capabilities/set_mode/status/{resp.json()['taskId']}")

POST(f"/v1/devices/{deviceId}/capabilities/approach_object/execute", {"arguments":{"TargetType":"pinkball"}}) # 

POST(f"/v1/devices/{deviceId}/capabilities/kick_object/execute",{"arguments":{"TargetType":"pinkball","KickMotion":"kick"}} ) # 
