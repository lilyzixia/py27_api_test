''' 
author:紫夏
Time:2020/3/29 23:53
'''
import os
import unittest
import decimal
from library.myddt import ddt,data
from common.Handler_excel import Handler_Excel
from common.handler_path import DATA_DIR
from common.handler_config import conf
from requests import request
from jsonpath import jsonpath
from common.Handler_Logging import log
from common.handler_db import HandlerMysql
from common.handle_data import EnvData,replace_data
from common.handle_Login1 import LoginBase

filename=os.path.join(DATA_DIR,'cases.xlsx')

@ddt
class TestRecharge(unittest.TestCase,LoginBase):
    excel=Handler_Excel(filename,'recharge')
    cases=excel.read_data()
    db=HandlerMysql()

    @classmethod
    def setUpClass(cls):
        LoginBase.login()

    @data(*cases)
    def test_recharge(self,case):
        # pass

        url=conf.get('env','base_url')+case['url']
        method=case['method']
        # 1.准备用例数据
        # 替换用户id,转换为字典
        data=eval(replace_data(case['data']))

        # 2.准备请求头
        headers=eval(conf.get('env','headers'))
        headers['Authorization']=getattr(EnvData,'token')

        expected=eval(case['expected'])
        row=case['case_id']+1

        # 判断该用例是否需要数据库校验
        if case['check_sql']:
            sql = replace_data(case['check_sql'])
            res_db = self.db.find_one(sql)
            start_money = res_db['leave_amount']
            print('充值前金额：', start_money)


        # 2.发送请求，获取实际结果
        response=request(method=method,url=url,headers=headers,json=data)
        res=response.json()

        print('预期结果', expected)
        print('实际结果', res)

        # 获取充值之后的账户余额
        if case['check_sql']:
            sql = replace_data(case['check_sql'])
            res_db = self.db.find_one(sql)
            end_money = res_db['leave_amount']
            print('充值后金额：', end_money)


        # # 3.断言预期结果和实际结果
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if case['check_sql']:
                # 将充值金额转换为decimal类型，因为数据库是decimal类型的
                recharge_money=decimal.Decimal(str(data['amount']))
                self.assertEqual(recharge_money,end_money-start_money)
        except AssertionError as e:
            log.error('用例--{}--执行不通过'.format(case['title']))
            log.exception(e)
            log.debug('预期结果:{}'.format(expected))
            log.debug('实际结果:{}'.format(res))

            self.excel.write_data(row=row,column=8,value='fail')

            raise e
        else:
            log.info('用例--{}--执行通过'.format(case['title']))
            self.excel.write_data(row=row, column=8, value='pass')
