''' 
author:紫夏
Time:2020/4/2 2:00
'''


'''
审核接口
    前置条件：
    1.管理员登录
    2.有待审核的项目
        添加项目前普通用户登录


'''
import unittest
import os
from requests import request
from library.myddt import ddt,data
from common.handler_db import HandlerMysql
from common.handler_path import DATA_DIR
from common.handler_config import conf
from common.Handler_excel import Handler_Excel
from jsonpath import jsonpath
from common.Handler_Logging import log
from common.handle_data import EnvData,replace_data
from common.handle_Login1 import LoginBase



@ddt
class AuditTestCase(unittest.TestCase):
    filename=os.path.join(DATA_DIR,'cases.xlsx')
    excel=Handler_Excel(filename,'audit')
    cases = excel.read_data()
    db=HandlerMysql()



    @classmethod
    def setUpClass(cls):
        # 所有用例执行前的前置条件：管理员登录、普通用户登录
        LoginBase.login()
        LoginBase.admin_login()

        # url = conf.get('env', 'base_url') + '/member/login'
        # headers = eval(conf.get('env', 'headers'))
        # # 1、管理员登录
        # admin_data={'mobile_phone':conf.get('test_data','admin_phone'),
        #         'pwd':conf.get('test_data','admin_pwd')}
        #
        # # 2.普通用户登录
        # user_data = {'mobile_phone':conf.get('test_data','phone'),
        #         'pwd':conf.get('test_data','pwd')}
        #
        # response1=request(method='post',url=url,json=admin_data,headers=headers)
        # res1=response1.json()
        # cls.admin_token='Bearer' + ' ' +jsonpath(res1,'$..token')[0]
        #
        #
        # response2=request(method='post',url=url,json=user_data,headers=headers)
        # res2=response2.json()
        # cls.user_token = 'Bearer' + ' ' + jsonpath(res2, '$..token')[0]
        # cls.user_member_id = str(jsonpath(res2, '$..id')[0])
        #


    def setUp(self):
    #     每条用例执行的前置条件：添加一个新的项目
        url = conf.get('env', 'base_url') + '/loan/add'
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization']=getattr(EnvData,'token')
        data={"member_id":getattr(EnvData,'member_id'),
              "title":"贷款买楼666",
              "amount":1000,
                "loan_rate":1,
                "loan_term":1,
                "loan_date_type":1,
                 "bidding_days":1}
        # 发送请求，添加项目
        response=request(method='post',url=url,json=data,headers=headers)
        res=response.json()
        loan_id=str(jsonpath(res,'$..id')[0])
        setattr(EnvData, 'loan_id', loan_id)
        # print('项目id', self.loan_id)


    @data(*cases)
    def test_audit(self,case):
# 1.准备数据
        url=conf.get('env','base_url')+case['url']
        if '#pass_loan_id#' in case['data']:
            data=eval(replace_data(case['data']))
            # data = eval(case['data'].replace('#loan_id#', self.loan_id))



        data=eval(replace_data(case['data']))
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization']=getattr(EnvData,'admin_token')

        if case['title']=='普通用户审核':
            headers['Authorization']=getattr(EnvData,'token')

        method=case['method']
        expected=eval(case['expected'])
        row=case['case_id']+1

        response=request(method=method,url=url,json=data,headers=headers)
        res=response.json()
        print(res)
        print(expected)
        if case['title']=='审核通过' and  case['case_id']==1:
            AuditTestCase.pass_loan_id=data['loan_id']

# 3.断言
        try:
            self.assertEqual(res['code'],expected['code'])
            self.assertEqual(res['msg'],expected['msg'])
            if case['check_sql']:
                # 原方法
                # case['check_sql'] = case['check_sql'].replace('#loan_id#',self.loan_id)
                # res = self.db.find_one(case['check_sql'])
                # res2 = res['status']
                # self.assertEqual(res2, expected['status'])

                # 新方法
                sql = replace_data(case['check_sql'])
                # case['check_sql'].replace('#loan_id#',self.loan_id)
                status=self.db.find_one(sql)['status']
                self.assertEqual(status, expected['status'])

        except AssertionError as e:
            log.error('用例----{}----执行不通过'.format(case['title']))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value='fail')
            log.debug('预期结果', expected)
            log.debug('实际结果', res)

            raise e
        else:
            log.info('用例----{}----执行通过'.format(case['title']))
            self.excel.write_data(row=row, column=8, value='pass')
