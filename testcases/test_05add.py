''' 
author:紫夏
Time:2020/4/1 22:57
'''


'''
一、添加项目
    前置条件：登录
    普通用户添加项目，管理员审核项目
    年利率0-24
    
    加标之前查询该用户对应的标数量
    加标之后查询该用户对应的标数量
    校验是否新增一条标记录
    

'''
import unittest
import os
from library.myddt import ddt,data
from common.Handler_excel import Handler_Excel
from common.handler_config import conf
from requests import request
from jsonpath import jsonpath
from common.handler_path import DATA_DIR
from common.handler_db import HandlerMysql
from common.Handler_Logging import log
from common.handle_data import replace_data,EnvData
from common.handle_Login1 import LoginBase

@ddt
class AddTestCase(unittest.TestCase):
    filename=os.path.join(DATA_DIR,'cases.xlsx')
    excel=Handler_Excel(filename,'add')
    cases=excel.read_data()
    db=HandlerMysql()


    @classmethod
    def setUpClass(cls):
        LoginBase.login()
        # headers=eval(conf.get('env','headers'))
        # url=conf.get('env','base_url')+'/member/login'
        # data={'mobile_phone':conf.get('test_data','phone'),
        #         'pwd':conf.get('test_data','pwd')}
        # response1=request(method='post',headers=headers,json=data,url=url)
        # res1=response1.json()
        # member_id=str(jsonpath(res1,'$..id')[0])
        # token='Bearer'+' '+jsonpath(res1,'$..token')[0]
        # #将提取出来的数据保存为EnvData的类属性（环境变量）
        # setattr(EnvData,'member_id',member_id)
        # setattr(EnvData,'token',token)
        # print(token)
        # print(member_id)

    #
    @data(*cases)
    def test_add(self,case):

        url = conf.get('env', 'base_url') + case['url']
        method=case['method']

        headers=eval(conf.get('env', 'headers'))
        headers['Authorization']=getattr(EnvData,'token')

        # 替换用例中的member_Id
        # case['data']=case['data'].replace('#member_id#',self.member_id)
        data=eval(replace_data(case['data']))

        expected=eval(case['expected'])
        row=case['case_id']+1

        # 加标之前查询该用户对应的标数量
        if case['check_sql']:
            # sql = case['check_sql'].replace('#member_id#', self.member_id)
            sql = replace_data(case['check_sql'])
            start_count = self.db.find_count(sql)

        response2=request(method=method,headers=headers,json=data,url=url)
        res2=response2.json()
        print('预期结果', expected)
        print('实际结果', res2)

        try:
            self.assertEqual(expected['code'],res2['code'])
            self.assertEqual(expected['msg'], res2['msg'])
            # 加标之后
            if case['check_sql']:
                sql = replace_data(case['check_sql'])
                end_count = self.db.find_count(sql)
                print(end_count-start_count)
                # self.assertEqual(1,end_count-start_count)

        except AssertionError as e:
            log.error('用例----{}----执行不通过'.format(case['title']))
            log.exception(e)
            self.excel.write_data(row=row,column=8,value='不通过')
            log.debug(expected)
            log.debug(res2)
            raise e
        else:
            log.info('用例----{}----执行通过'.format(case['title']))
            self.excel.write_data(row=row, column=8, value='通过')









