''' 
author:紫夏
Time:2020/4/9 1:41
'''


'''
投资接口的前置条件
1、有项目： 借款人登陆——>创建项目
           管理员登陆——>审核通过
2、用户有钱
    投资人（普通用户）登陆——>充值

执行投资相关的用例

'''

import unittest
import os
from library.myddt import ddt,data
from common.Handler_excel import Handler_Excel
from common.handler_path import DATA_DIR
from common.handler_config import conf
from common.handle_data import replace_data,EnvData
from requests import request
from jsonpath import jsonpath
from common.Handler_Logging import log
from common.handler_db import HandlerMysql
from decimal import Decimal

filename=os.path.join(DATA_DIR,'cases.xlsx')

@ddt
class InvestTestCase(unittest.TestCase):
    excel=Handler_Excel(filename,'invest')
    cases=excel.read_data()
    sql=HandlerMysql()

    @data(*cases)
    def test_invest(self,case):
#         1.准备数据
        url=conf.get('env','base_url')+case['url']
        method=case['method']
        headers=eval(conf.get('env','headers'))
        if case['interface'] !='login':
        #     如果不是登陆接口，则添加一个token
            headers['Authorization']=getattr(EnvData,'token')
        data=eval(replace_data(case['data']))
        expected=eval(case['expected'])
        row=case['case_id']+1

#       获取需要sql校验的数据：
        if case['check_sql']:
            sql1='select leave_amount from futureloan.member where member_id = #member_id#'.replace('#member_id#',getattr(EnvData,'member_id'))
            sql2 = 'select * from futureloan.invest where member_id= #member_id#;'.replace('#member_id#',getattr(EnvData,'member_id'))
            sql3 = 'select * from futureloan.financelog where pay_member_id= #member_id#;'.replace(getattr(EnvData,'member_id'))
            start_amount=self.sql.find_one(sql1)
            start_invest_num=self.sql.find_count(sql2)
            start_financelog_num=self.sql.find_count(sql3)


# 2.发送请求，获取实际结果
        response=request(url=url,json=data,method=method,headers=headers)
        res=response.json()
    #   登录需要提取Id和token
        # 加标需要提取标id
        if case['interface']=='login':
#             如果是登录接口，需要提取member_id
            member_id=str(jsonpath(res,'$..id')[0])
            token='Bearer'+' '+jsonpath(res,'$..token')[0]
            setattr(EnvData,'member_id',member_id)
            setattr(EnvData,'token',token)
        if case['interface']=='add':
#            如果是加标接口，则提取loan_id
            loan_id=str(jsonpath(res,'$..id')[0])
            setattr(EnvData,'loan_id',loan_id)


# 3.断言
            try:
                self.assertEqual(res['code'], expected['code'])
                self.assertEqual(res['msg'], expected['msg'])
                if case['check_sql']:
                    sql1 = 'select leave_amount from futureloan.member where member_id = #member_id#'.replace(
                        '#member_id#', getattr(EnvData, 'member_id'))
                    sql2 = 'select * from futureloan.invest where member_id= #member_id#;'.replace('#member_id#',getattr(EnvData,'member_id'))
                    sql3 = 'select * from futureloan.financelog where pay_member_id= #member_id#;'.replace('#member_id#',getattr(EnvData, 'member_id'))
                    after_amount = self.sql.find_one(sql1)
                    self.assertEqual(after_amount-start_amount, Decimal(str(data['amount'])))
                    after_invest_num = self.sql.find_count(sql2)
                    self.assertEqual(after_invest_num - start_invest_num, 1)
                    after_financelog_num = self.sql.find_count(sql3)
                    self.assertEqual(after_financelog_num - start_financelog_num, 1)
                    if '满标' in case['title']:
                        sql4 = 'select id from futureloan.invest where loan_id= {};'.format(getattr(EnvData,'loan_id'))
                        invest_ids=self.sql.find_all(sql4)
                        for i in invest_ids:
                            sql5 = 'select * from futureloan.repayment where invest_id= {};'.format(i)
                            repayment_num = self.sql.find_count(sql5)
                            self.assertTrue(repayment_num)
                # if case['check_sql']:
                #
                #     sql = case['check_sql'].replace('#loan_id#', self.loan_id)
                #     status = self.db.find_one(sql)['status']
                #     self.assertEqual(status, expected['status'])

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







