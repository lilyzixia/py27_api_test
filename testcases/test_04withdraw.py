''' 
author:紫夏
Time:2020/3/31 2:02
'''

import os
import unittest
from library.myddt import ddt,data
from common.Handler_excel import Handler_Excel
from common.handler_path import DATA_DIR
from common.handler_config import conf
from requests import request
from jsonpath import jsonpath
from common.handler_db import HandlerMysql
from common.Handler_Logging import log
import decimal
from common.handle_Login1 import LoginBase
from common.handle_data import EnvData,replace_data


@ddt
class WithdrawTestCase(unittest.TestCase):
    filename=os.path.join(DATA_DIR,'cases.xlsx')
    excel=Handler_Excel(filename,'withdraw')
    cases=excel.read_data()
    db=HandlerMysql()

    @classmethod
    def setUpClass(cls):
        LoginBase.login()



    @data(*cases)
    def test_withdraw(self,case):


        url=conf.get('env','base_url')+case['url']
        method=case['method']

        # case['data']=case['data'].replace('#member_id#',self.member_id)
        # data=eval()
        data=eval(replace_data(case['data']))

        headers=eval(conf.get('env','headers'))
        headers['Authorization']=getattr(EnvData,'token')

        expected=eval(case['expected'])
        row=case['case_id']+1

        if case['check_sql']:
            case['check_sql']=replace_data(case['check_sql'])
            res_before=self.db.find_one(case['check_sql'])
            money_before=res_before['leave_amount']
            print('提现前金额',money_before)


        response1=request(method=method,url=url,headers=headers,json=data)
        res1=response1.json()
        print('预期结果', expected)
        print('实际结果', res1)


        if case['check_sql']:
            case['check_sql']=replace_data(case['check_sql'])
            res_before=self.db.find_one(case['check_sql'])
            money_after=res_before['leave_amount']
            print('提现后金额',money_after)

        try:
            self.assertEqual(expected['code'],res1['code'])
            self.assertEqual(expected['msg'],res1['msg'])
            if case['check_sql']:
                self.assertEqual(decimal.Decimal(str(data['amount'])),money_before-money_after )
        except AssertionError as e:
            log.error('用例----{}----执行不通过'.format(case['title']))
            log.exception(e)
            self.excel.write_data(row=row,column=8,value='fail')
            log.debug('预期结果', expected)
            log.debug('实际结果', res1)

            raise e
        else:
            log.info('用例----{}----执行通过'.format(case['title']))
            self.excel.write_data(row=row, column=8, value='pass')






