import requests, os, yaml
url ="https://public.api.aibo.com"
with open("config.yaml") as f:
    token = yaml.load(f, Loader=yaml.FullLoader)["token"]
headers = {
    "Authorization": f"Bearer {token}",
}
resp = requests.get(url+"/v1/devices", headers=headers)
print(resp.json())