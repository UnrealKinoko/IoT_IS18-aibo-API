#POST() GET()のhead部は暫定的な処理 あとで変更する ちかれた

import requests, yaml, time, random# ライブラリのインポート requestsはAPIを叩くためのライブラリ、yamlは設定ファイルを読み込むためのライブラリ timeは時間を扱うライブラリ randomは乱数を生成するライブラリ

url ="https://public.api.aibo.com" # aiboのAPIのURL
with open("config.yaml") as f: # config.yamlを読み込む
    token = yaml.load(f, Loader=yaml.SafeLoader)["kicker"]["token"] # config.yamlのtokenを取得
    print("token loaded")

with open("config.yaml") as f: # 同上 一つにまとめると動かなかった 後で調べる
    tokenB= yaml.load(f, Loader=yaml.SafeLoader)["keeper"]["token"]

headers = {"Authorization": f"Bearer {token}",} # ヘッダーの設定 AuthorizationにBearer +APIトークンを設定
headersB = {"Authorization": f"Bearer {tokenB}",}
def statCodeBranch(urlSuf,resp): # ステータスコードによって分岐する関数 例外を発生させる
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

def POST(head,urlSuf,json): # POSTリクエストを送る関数 urlSufはURLの後ろに追加する文字列、jsonは送信するjson
    for i in range(3):
        print(f"POST:{url}{urlSuf} >> ",end="")
        resp= requests.post(url+urlSuf, headers=head, json=json) # POSTリクエストを送信
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

def GET(head,urlSuf): # GETリクエストを送る関数 urlSufはURLの後ろに追加する文字列
    for i in range(3):
        print(f"GET:{url}{urlSuf} >> ",end="")
        resp= requests.get(url+urlSuf, headers=head) # GETリクエストを送信
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

deviceId = GET(headers,"/v1/devices").json()["devices"][0]["deviceId"] # デバイスIDを取得 今回は一つのデバイスのみを想定
deviceIdB= GET(headersB,"/v1/devices").json()["devices"][0]["deviceId"] 

resp = POST(headers,f"/v1/devices/{deviceId}/capabilities/set_mode/execute", {"arguments":{"ModeName":"DEVELOPMENT"}}) # 指示待ちモードに設定
while GET(headers,f"/v1/executions/{resp.json()["executionId"]}").json()["status"] != "SUCCEEDED": # 完了するまで待機
    print(GET(headers,f"/v1/executions/{resp.json()["executionId"]}").json()["status"])
    time.sleep(5)

resp = POST(headersB,f"/v1/devices/{deviceIdB}/capabilities/set_mode/execute", {"arguments":{"ModeName":"DEVELOPMENT"}}) # 指示待ちモードに設定
while GET(headersB,f"/v1/executions/{resp.json()["executionId"]}").json()["status"] != "SUCCEEDED": # 完了するまで待機
    print(GET(headersB,f"/v1/executions/{resp.json()["executionId"]}").json()["status"])
    time.sleep(5)

diceA= random.randint(0,2)
diceB= random.randint(0,2)

match diceA:
    case 0:
        # move left
        respA= POST(headers,f"/v1/devices/{deviceId}/capabilities/move_sideways/execute",{"arguments":{"WalkSpeed":1,"WalkDistance":-0.4}})
    case 1:
        pass
    case 2:
        respA= POST(headers,f"/v1/devices/{deviceId}/capabilities/move_sideways/execute",{"arguments":{"WalkSpeed":1,"WalkDistance":0.4}})

match diceB:
    case 0:
        # move right
        respB= POST(headersB,f"/v1/devices/{deviceIdB}/capabilities/move_sideways/execute",{"arguments":{"WalkSpeed":1,"WalkDistance":-0.2}})
    case 1:
        pass
    case 2:
        respB= POST(headersB,f"/v1/devices/{deviceIdB}/capabilities/move_sideways/execute",{"arguments":{"WalkSpeed":1,"WalkDistance":0.2}})

while GET(headers,f"/v1/executions/{respA.json()["executionId"]}").json()["status"] != "SUCCEEDED": # 完了するまで待機
    print(GET(headers,f"/v1/executions/{respA.json()["executionId"]}").json()["status"])
    time.sleep(1)

while GET(headersB,f"/v1/executions/{respB.json()["executionId"]}").json()["status"] != "SUCCEEDED": # 完了するまで待機
    print(GET(headersB,f"/v1/executions/{respB.json()["executionId"]}").json()["status"])
    time.sleep(1)

POST(headers,f"/v1/devices/{deviceId}/capabilities/approach_object/execute", {"arguments":{"TargetType":"pinkball"}}) # 

resp= POST(headers,f"/v1/devices/{deviceId}/capabilities/kick_object/execute",{"arguments":{"TargetType":"pinkball","KickMotion":"kick"}} ) # 

while GET(headers,f"/v1/executions/{resp.json()["executionId"]}").json()["status"] != "SUCCEEDED": # 完了するまで待機
    print(GET(headers,f"/v1/executions/{resp.json()["executionId"]}").json()["status"])
    time.sleep(1)

if diceA != diceB:
    print("kicker win")
    POST(headers,f"/v1/devices/{deviceId}/capabilities/play_trick/execute",{"arguments":{"TrickName":"waltzOfTheFlowers"}})
    POST(headersB,f"/v1/devices/{deviceIdB}/capabilities/play_motion/execute",{"arguments":{"Category":"relax","Mode":"NONE"}})
else:
    print("keeper win")
    POST(headersB,f"/v1/devices/{deviceIdB}/capabilities/play_trick/execute",{"arguments":{"TrickName":"waltzOfTheFlowers"}})
    POST(headers,f"/v1/devices/{deviceId}/capabilities/play_motion/execute",{"arguments":{"Category":"relax","Mode":"NONE"}})