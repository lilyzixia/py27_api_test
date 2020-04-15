''' 
author:紫夏
Time:2020/4/11 1:31
'''
from common.handler_config import conf
from requests import request
from jsonpath import jsonpath
from common.handle_data import replace_data,EnvData


class LoginBase():

    @staticmethod
    def login():
        url=conf.get('env','base_url')+'/member/login'
        data={
            'mobile_phone':conf.get('test_data','phone'),
            'pwd':conf.get('test_data','pwd')
        }
        headers=eval(conf.get('env','headers'))
        response=request(method='post',url=url,json=data,headers=headers)
        res=response.json()
        member_id=str(jsonpath(res,'$..id')[0])
        token='Bearer'+' '+jsonpath(res,'$..token')[0]
        setattr(EnvData,'member_id',member_id)
        setattr(EnvData,'token',token)

    @staticmethod
    def admin_login():
        url=conf.get('env','base_url')+'/member/login'
        data={
            'mobile_phone':conf.get('test_data','admin_phone'),
            'pwd':conf.get('test_data','admin_pwd')
        }
        headers=eval(conf.get('env','headers'))
        response=request(method='post',url=url,json=data,headers=headers)
        res=response.json()
        admin_member_id=str(jsonpath(res,'$..id')[0])
        admin_token='Bearer'+' '+jsonpath(res,'$..token')[0]
        setattr(EnvData,'admin_member_id',admin_member_id)
        setattr(EnvData,'admin_token',admin_token)

    @staticmethod
    def invest_login():
        url=conf.get('env','base_url')+'/member/login'
        data={
            'mobile_phone':conf.get('test_data','invest_phone'),
            'pwd':conf.get('test_data','invest_pwd')
        }
        headers=eval(conf.get('env','headers'))
        response=request(method='post',url=url,json=data,headers=headers)
        res=response.json()
        invest_member_id=str(jsonpath(res,'$..id')[0])
        invest_token='Bearer'+' '+jsonpath(res,'$..token')[0]
        setattr(EnvData,'invest_member_id',invest_member_id)
        setattr(EnvData,'invest_token',invest_token)



