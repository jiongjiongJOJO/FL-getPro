import os,requests,json,re
from tempmail import TemporaryEmail

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

def checkUserExist(user,type,):
    headers = {
        'User-Agent': 'okhttp/4.2.2',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data_json = {
    "loginName": user,
    "loginType": type,
    "deviceId": "547f6feb12d6411d",
    "deviceModel": "OnePlus HD1900",
    "deviceSdkCode": 29,
    "deviceSdkName": "10",
    "flavor": "CN",
    "language": "zh",
    "packageName": "com.lerist.fakelocation",
    "timezone": "GMT+08:00",
    "versionCode": "906",
    "versionName": "1.2.1.8"
    }
    response = requests.post('http://fakelocation.api.lerist.cc:8000/FakeLocation/user/checkUserExist', json=data_json,
                             headers=headers)
    return response.text

def sendEmailCode(user):
    headers = {
        'User-Agent': 'okhttp/4.2.2',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    data_json = {
        "deviceId": "547f6feb12d6411d",
        "emailAddress": user,
        "timezone": "GMT+08:00",
        "type": "login"
    }
    response = requests.post('http://fakelocation.api.lerist.cc:8000/FakeLocation/user/requestEmailVercode', json=data_json,
                             headers=headers)
    return response.text

def regAccount(user,code):
    headers = {
    'User-Agent': 'okhttp/4.2.2',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/json; charset=UTF-8'
    }
    data_json ={
    "loginName": user,
    "loginType": "email",
    "vercode": code,
    "deviceId": "547f6feb12d6411d",
    "deviceModel": "OnePlus HD1900",
    "deviceSdkCode": 29,
    "deviceSdkName": "10",
    "flavor": "CN",
    "language": "zh",
    "packageName": "com.lerist.fakelocation",
    "timezone": "GMT+08:00",
    "versionCode": "906",
    "versionName": "1.2.1.8"
}
    response = requests.post('http://fakelocation.api.lerist.cc:8000/FakeLocation/user/login',json=data_json,headers=headers)
    return response.text




password = '123456789'
type = 'email'
send_key = os.getenv("SEND")

while True:
    email = TemporaryEmail()
    user = email.get_email_address()
    if('用户不存在' in checkUserExist(user,type)):
        break
sendEmailCode(user)
while True:
    if(email.check_received_email()):
        break
email_content = email.get_email_content()

pattern = '&lt;a href=&#34;#&#34;&gt;(.*)</a>&lt;/a&gt;&lt;/span&gt'
emailCode = (re.findall(pattern,email_content[0])[0])
reg_info = regAccount(user,emailCode)
if(json.loads(reg_info).get('success')):
    token = json.loads(reg_info).get('body')['token']
    getpro_info = getpro(token)
    getpro_code = json.loads(getpro_info).get('code')
    if(getpro_code == 200):
        print(json.loads(getpro_info).get('message'))
        push(send_key, 'FakeLocation 账号', user+'<br>'+getpro_info)
    else:
        print(getpro_info)
        push(send_key, 'FakeLocation 失败', getpro_info)
else:
    print(reg_info)
    push(send_key, 'FakeLocation 失败', reg_info)

