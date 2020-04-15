''' 
author:紫夏
Time:2020/4/6 16:24
'''



import unittest
import os
from common.handler_path import DATA_DIR
from common.Handler_excel import Handler_Excel
from library.myddt import ddt,data
from common.handler_config import conf
from requests import request
from jsonpath import jsonpath
from common.Handler_Logging import log
from common.handle_data import EnvData
from common.handle_Login1 import LoginBase

filename=os.path.join(DATA_DIR,'cases.xlsx')

@ddt
class LoansTestCase(unittest.TestCase):
    excel=Handler_Excel(filename,'loans')
    cases=excel.read_data()

    # @classmethod
    # def setUpClass(cls):
    #     LoginBase.login()



    @data(*cases)
    def test_loans(self,case):
        url=conf.get('env','base_url')+case['url']
        method=case['method']
        headers=eval(conf.get('env','headers'))
        # headers['Authrization']=getattr(EnvData,'token')
        data=eval(case['data'])
        expected=eval(case['expected'])
        row=case['case_id']+1
        response2=request(method=method,params=data,url=url,headers=headers)
        res2=response2.json()
        print('预期结果：',expected)
        print('实际结果：',res2)


        try:
            self.assertEqual(expected['code'], res2['code'])
            self.assertEqual(expected['msg'], res2['msg'])
        #     可以进行返回数据条数的校验
            self.assertEqual(expected['len'],len(res2['data']))
        except AssertionError as e:
            log.error('用例----{}----执行不通过'.format(case['title']))
            log.exception(e)
            log.debug('预期结果', expected)
            log.debug('实际结果', res2)
            self.excel.write_data(row=row, column=8, value='不通过')
            raise e
        else:
            log.info('用例----{}----执行通过'.format(case['title']))
            self.excel.write_data(row=row, column=8, value='通过')



