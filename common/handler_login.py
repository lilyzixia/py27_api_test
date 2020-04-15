''' 
author:紫夏
Time:2020/4/6 17:07
'''

from common.handler_config import conf
from requests import request
from jsonpath import jsonpath


class Login_setup():
    headers = eval(conf.get('env', 'headers'))
    url = conf.get('env', 'base_url') + '/member/login'
    data = {'mobile_phone': conf.get('test_data', 'phone'),
            'pwd': conf.get('test_data', 'pwd')}


    # @classmethod
    def login(self):
        response1 = request(method='post', headers=self.headers, json=self.data, url=self.url)
        res1 = response1.json()
        member_id = str(jsonpath(res1, '$..id')[0])
        token1 = jsonpath(res1, '$..token')[0]
        return member_id,token1
        # return member_id


login=Login_setup()
# id,token=s.login()
# print(id,token)