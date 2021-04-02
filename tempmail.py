# encoding:utf-8
import requests,random,re


class TemporaryEmail:
    def __init__(self):
        char = '0123456789abcdefghijklmnopqrstuvwxyz'
        user_len = random.randint(6,12)
        self.name = ''
        for i in range(user_len):
            self.name += char[random.randint(0,len(char)-1)]
        data = {
            'user': self.name,
            'domain': 'tm.zakx.de'
        }
        a = requests.post('http://tm.zakx.de/redirect',data=data)
    def get_email_address(self):
        return self.name+'@tm.zakx.de'

    def check_received_email(self):
        # 发送刷新检查是否有邮件并得到邮件id
        response = requests.get('http://tm.zakx.de/'+self.get_email_address()+'/')
        if('There are no mails for' in response.text):
            return False
        else:
            pattern = '<a href="/'+self.get_email_address()+'/(.*)/">&#34;Fake Location&#34; &lt;support@lanes.cc&gt;'
            self.id = re.findall(pattern, response.text)[0]
            return True

    def get_email_content(self):

        # 获取邮件内容

        response = requests.get('http://tm.zakx.de/'+self.get_email_address()+'/'+self.id+'/')
        return (response.text)
