''' 
author:紫夏
Time:2020/3/29 0:35
'''

import unittest
from common.Handler_excel import Handler_Excel
from library.myddt import ddt,data
from common.handler_config import conf
from requests import request
from common.Handler_Logging import log
from common.handler_path import DATA_DIR
import os

filename = os.path.join(DATA_DIR,'cases.xlsx')
@ddt
class LoginTestCase(unittest.TestCase):
    excel=Handler_Excel(filename,'login')
    cases=excel.read_data()


    @data(*cases)
    def test_login(self,case):
        method=case['method']
        url=conf.get('env','base_url')+(case['url'])
        headers=eval(conf.get('env','headers'))
        data=eval(case['data'])
        expected=eval(case['expected'])
        row=case['case_id']+1

        response=request(method=method,url=url,headers=headers,json=data)
        res=response.json()
        # print(res)

        print('预期结果',expected)
        print('实际结果',res)

        try:
            self.assertEqual(res['code'],expected['code'])
            self.assertEqual(res['msg'],expected['msg'])
        except AssertionError as e:

            log.error('用例--{}--执行不通过'.format(case['title']))
            log.exception(e)
            log.debug('预期结果:{}'.format(expected))
            log.debug('实际结果:{}'.format(res))
            self.excel.write_data(row=row,column=8,value='fail')
            raise e
        else:
            self.excel.write_data(row=row, column=8, value='pass')
            log.info('用例--{}--执行通过'.format(case['title']))












