import os,requests,json

def push(key,title,content):

    url = 'http://pushplus.hxtrip.com/send'
    data = {
        "token": key,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)

def login(user,password,type):
    headers = {
    'User-Agent': 'okhttp/4.2.2',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/json; charset=UTF-8'
    }
    data_json = {"loginName":user,"loginPwd":password,"loginType":type,"deviceId":"547f6feb12d6411d","deviceModel":"OnePlus HD1900","deviceSdkCode":29,"deviceSdkName":"10","flavor":"CN","language":"zh","packageName":"com.lerist.fakelocation","timezone":"GMT+08:00","versionCode":"906","versionName":"1.2.1.8"}
    response = requests.post('http://fakelocation.api.lerist.cc:8000/FakeLocation/user/login',json=data_json,headers=headers)
    return response.text

def getpro(token):
    headers = {
    'User-Agent': 'okhttp/4.2.2',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/json; charset=UTF-8'
    }
    data_json = {"deviceId":"547f6feb12d6411d","deviceModel":"OnePlus HD1900","deviceSdkCode":29,"deviceSdkName":"10","flavor":"CN","language":"zh","packageName":"com.lerist.fakelocation","timezone":"GMT+08:00","token":token,"versionCode":"906","versionName":"1.2.1.8"}
    response = requests.post('http://fakelocation.api.lerist.cc:8000/FakeLocation/user/trypro', json=data_json,headers=headers)
    return response.text


user = os.getenv("user")
password = os.getenv("password")
type = os.getenv("type")
if(type == ''):
    type = 'email'
send_key = os.getenv("SEND")
login_info = login(user,password,type)
login_code = json.loads(login_info).get('code')
if(login_code == 200):
    token = json.loads(login_info).get('body')['token']
    getpro_info = getpro(token)
    getpro_code = json.loads(getpro_info).get('code')
    if(getpro_code == 200):
        print(json.loads(getpro_info).get('message'))
    else:
        print(getpro_info)
        push(send_key, 'FakeLocation 失败', getpro_info)