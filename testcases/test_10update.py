''' 
author:紫夏
Time:2020/4/5 23:20
'''


import unittest
import os
from library.myddt import ddt,data
from common.Handler_excel import Handler_Excel
from common.handler_path import DATA_DIR
from common.handler_config import conf
from requests import request
from jsonpath import jsonpath
from common.handler_db import HandlerMysql
from common.Handler_Logging import log
from common.handle_data import EnvData
from common.handle_Login1 import LoginBase,replace_data

@ddt
class UpdateTestCase(unittest.TestCase):
    excel=Handler_Excel(os.path.join(DATA_DIR,'cases.xlsx'),'update')
    cases=excel.read_data()
    db=HandlerMysql()

    @classmethod
    def setUpClass(cls):
        LoginBase.login()
        # url=conf.get('env','base_url')+'/member/login'
        # headers=eval(conf.get('env','headers'))
        # data1={'mobile_phone':eval(conf.get('test_data','phone')),
        #       'pwd':conf.get('test_data','pwd')
        #       }
        #
        # response1=request(method='POST',json=data1,url=url,headers=headers)
        # res1=response1.json()
        # cls.member_id=str(jsonpath(res1,'$..id')[0])
        # cls.token='Bearer' + ' ' +jsonpath(res1,'$..token')[0]
        # print(member_id)
        # print(token)

    @data(*cases)
    def test_update(self,case):
        method=case['method']
        url=conf.get('env','base_url')+case['url']
        headers=eval(conf.get('env','headers'))
        headers['Authorization']=getattr(EnvData,'token')
        expected=eval(case['expected'])
        row=case['case_id']+1
        if '#member_id#' in case['data']:
            # case['data']=case['data'].replace('#member_id#',self.member_id)
            data=eval(replace_data(case['data']))
        response2=request(method=method,json=data,url=url,headers=headers)
        res2=response2.json()
        print('预期结果',expected)
        print('实际结果',res2)
        #
        #
        try:
            self.assertEqual(res2['code'],expected['code'])
            self.assertEqual(res2['msg'],expected['msg'])
            if case['check_sql']:
                sql=replace_data(case['check_sql'])
                reg_name1=self.db.find_one(sql)['reg_name']
                self.assertEqual(reg_name1,data['reg_name'])
        except AssertionError as e:
            log.error('用例----{}----执行不通过'.format(case['title']))
            log.exception(e)
            self.excel.write_data(row=row,column=8,value='不通过')
            log.debug('预期结果',expected)
            log.debug('实际结果',res2)
            raise e
        else:
            log.info('测试用例----{}——----'.format(case['title']))
            self.excel.write_data(row=row,column=8,value='通过')
