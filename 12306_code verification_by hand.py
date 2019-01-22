import requests
import random

class Ticket_web:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'
        })    # 用户代理，隐藏身份，防止网站限制访问，下面的url抓包可以看到，有的只接受post请求，后面会模拟post请求
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image'    # 验证码图片
        self.passport_login_url = 'https://kyfw.12306.cn/passport/web/login'
        self.passport_check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.passport_auth_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        self.uamauthclient_url = 'https://kyfw.12306.cn/otn/uamauthclient'
        self.point = {
            '1': '35,42',
            '2': '108,42',
            '3': '185,42',
            '4': '254,42',
            '5': '34,115',
            '6': '108,115',
            '7': '180,115',
            '8': '258,115',
        }    # 切割每个小图片，模拟post发送鼠标的坐标
        self.dict = {}

    def get_point(self, nums):
        nums = nums.split(',')
        temp = []
        for item in nums:
            temp.append(self.point[item])
        return ','.join(temp)

    def main(self, username, password):    # 检查用户名&密码
        data = {
            'username': username,
            'password': password,
            'appid': 'otn'
        }
        self.session.get(self.login_url)
        self.get_captcha()
        check_res = self.check_captcha()
        if check_res:
            response = self.session.post(self.passport_login_url,data=data)
            if response.json()['result_code'] == 0:
                tk = self.get_tk()
                auth_res = self.get_auth(tk)

    def get_captcha(self):    # 获取验证码图片，会下载到项目目录中
        data = {
            'login_site': 'E',
            'module': 'login',
            'rand': 'sjrand',
            str(random.random()): ''
        }
        response = self.session.get(self.captcha_url,params=data)
        with open('captcha.jpg','wb') as f:
            f.write(response.content)

    def check_captcha(self):    # 验证码检查
        data = {
            'answer': self.get_point(input('请输入正确的图片序号：')),    # 两张图校验需要用","隔开
            'login_site': 'E',
            'rand': 'sjrand'
        }
        response = self.session.post(self.passport_check_captcha_url,data=data)
        if response.json()['result_code'] == '4':
            return True
        else:
            print('验证码错误，请重新运行并输入正确的图片序号！')
        return False

    def get_tk(self):    # 获取token
        uamtk_data = {
            'appid': 'otn'
        }
        response = self.session.post(self.passport_auth_url,data=uamtk_data)
        return response.json()['newapptk']

    def get_auth(self,tk):    # 获取权限
        auth_data = {
            'tk': tk
        }
        response = self.session.post(self.uamauthclient_url,data=auth_data)
        if response.json()['result_code'] == 0:
            print(response.text)
            return True
        return False

if __name__ == '__main__':
    ticket = Ticket_web()
    ticket.main(18888888888, 123456)    # 用户名&密码
