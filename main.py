
#!/usr/bin/python

# Dev Environment:
#   Ubuntu 20.04 focal(on the Windows Subsystem for Linux)
#   with Visual Studio Code

import os
import sys
import json
import requests

# POST API
url = 'https://gkdapp.strongmap.cn:9045/api/healthReportDd/add'

# POST header
hd = {
    'Connection': 'keep-alive',
    'Content-Length': '3813',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'xxxxxx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'XZT-CLIENTID': 'PC-001',
    'content-type': 'application/json;charset=UTF-8',
    'Referer': 'https://servicewechat.com/wxe9c88300c9903b6d/55/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br',
}

if __name__ == '__main__':
    # Check Files
    if not os.path.exists("noon.json") or not os.path.exists("morn.json"):
        print("ERROR: 'morn.json' or 'noon.json' Not Found")
        sys.exit(1)
    if not os.path.exists("userData.json"):
        print("ERROR: 'userData.json' Not Found!")
        sys.exit(1)
    
    # Load json files
    with open('morn.json', 'r', encoding='utf-8') as f:
        morn = json.load(f)
    with open('noon.json', 'r', encoding='utf-8') as f:
        noon = json.load(f)
    with open("./userData.json", 'r', encoding="utf-8") as f:
        uList = json.load(f)

    # ---- debug ----
    # print(f'{G}INFO{E}: ', morn)
    # print(f'{G}INFO{E}: ', noon)
    # sys.exit(0)
    # ---- debug ----