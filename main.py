
#!/usr/bin/python

# Dev Environment:
#   Ubuntu 20.04 focal(on the Windows Subsystem for Linux)
#   with Visual Studio Code

import os
import sys
import json
import time
import random
import requests
import datetime

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

# Get user data
def getUserChangeData(useid, token):
    # API
    get_url = 'https://gkdapp.strongmap.cn:9045/api/healthReportDd/getNewByUser'
    hd['Authorization'] = token
    header = hd
    data = json.dumps({"userId": useid}).encode('utf-8')
    result = requests.post(url=get_url, data=data, headers=header)

    # POST ERROR
    if result.status_code != 201:
        return None

    jdat = result.json()
    atProvince = jdat["atProvince"]
    atCity = jdat["atCity"]
    atDistrict = jdat["atDistrict"]
    userLocation = jdat["userLocation"]
    today = jdat["reportTime"][:11].strip()
    backSchoolTime = jdat["backSchoolTime"]
    now = str(datetime.date.today()).strip()
    # Reported
    if today == now:
        return 1
    # Return a list contains user data
    return [useid, atProvince, atCity, atDistrict, userLocation]

if __name__ == '__main__':
    # Check Files
    if not os.path.exists("noon.json") or not os.path.exists("morn.json"):
        print("ERROR: 'morn.json' or 'noon.json' Not Found")
        sys.exit(1)
    if not os.path.exists("userData.json"):
        print("ERROR: 'userData.json' Not Found!")
        sys.exit(1)
    elif os.path.getsize("userData.json") == 0:
        print("WARNING: 'userData.json' is Empty!")
    
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

    # Input Token and update POST header
    token = input("token:")
    if not token.startswith('Bearer '):
        print("ERROE: Wrong Token Format!")
        print("INFO: It should be 'Bearer xxxxxx'")
        sys.exit(1)
    hd['Authorization'] = token

# Change POST body
def changeBody(body, lst):
    body['userId'] = lst[0]
    body['atProvince'] = lst[1]
    body['atCity'] = lst[2]
    body['atDistrict'] = lst[3]
    body['userLocation'] = str(lst[4])
    return body

for n in range(len(uList)):
        u = random.sample(uList.keys(), 1)[0]  # py3.9 throw WARNNING
        print(f'INFO: Id:{u}, Name:{uList[u]["name"]}')
        # Get user info
        it = getUserChangeData(u, token)
        if it is None: # POST error
            print(f'ERROR: POST ERROR')
            del uList[u] # Del from user list
        elif it == 1: # Reported
            print(f'ERROR: Reported')
            del uList[u]
        else: # Normal
            if it[-1] != '1':  # user location is incorrect
                print(f"ERROR: user location error, ID:", u)
                del uList[u]
                continue
            else:
                print(f"INFO: ready to report!")
                # delay [2.0,5.0)s for each report
                delay = random.uniform(0.5, 2.0)
                time.sleep(delay)
                # remove user in dict if reported
                del uList[u]
            morn = changeBody(morn, it)
            noon = changeBody(noon, it)
            # Dump post body
            body_morning = json.dumps(morn).encode('utf-8')
            body_afternoon = json.dumps(noon).encode('utf-8')
            # POST for morning
            report_morn = requests.post(url, data=body_morning, headers=hd)
            tm = time.localtime()
            # POST for afternoon is opened after 11:58
            if tm.tm_hour < 11:
                print(f"INFO: H<11")
                continue
            elif tm.tm_hour == 11 and tm.tm_min < 58:
                print(f"INFO: H=11 & M<58")
                continue
            # Pause 1s for afternoon POST
            time.sleep(1)
            # POST for morning
            report_noon = requests.post(url, data=body_afternoon, headers=hd)