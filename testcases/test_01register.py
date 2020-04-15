''' 
author:紫夏
Time:2020/3/28 20:51
'''
'''



'''

import random
import unittest
import os
from common.Handler_excel import Handler_Excel
from library.myddt import ddt,data
from common.handler_config import conf
from requests import request
from common.Handler_Logging import log
from common.handler_path import DATA_DIR
from common.handler_db import HandlerMysql


filename = os.path.join(DATA_DIR,'cases.xlsx')


@ddt
class RegisterTestCase(unittest.TestCase):


    excel=Handler_Excel(filename,'register')
    cases=excel.read_data()
    db=HandlerMysql()

    @data (*cases)
    def test_register(self,case):
        # 第一步：准备用例数据

        # 请求方法
        method=case['method']
        # 请求地址
        url=conf.get('env','base_url')+case['url']
        # 请求参数
        # 判断是否有手机号码需要替换
        if '#phone#' in case['data']:
            # 随机生成一个手机号码
            phone=self.random_phone()
            # 将参数中的#phone#替换成随机生成的手机号
            case['data']=case['data'].replace('#phone#',phone)

        data=eval(case['data'])
        # 请求头  配置文件的请求头不能换行
        headers=eval(conf.get('env','headers'))
        expected=eval(case['expected'])
        row=case['case_id']+1

        # 第二步：发送请求，获取实际结果
        response=request(method=method,url=url,json=data,headers=headers)
        res=response.json()
        # print('实际结果：',res)
        # print(expected['code'])

        # 用print可以显示详细信息在报告上
        print('预期结果',expected)
        print('实际结果',res)

        # 第三步：断言
        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])

            # 判断是否需要sql校验
            if case['check_sql']:
                sql=case['check_sql'].replace('#phone#',data['mobile_phone'])

                # 方法1：是否可以找到数据
                # res=self.db.find_one(sql)
                # self.assertTrue(res)   #none为false??

                # 方法2：是否可以找到一条数据
                res=self.db.find_count(sql)
                self.assertEqual(1,res)

        except AssertionError as e:
            log.error('用例--{}--执行不通过'.format(case['title']))
            log.exception(e)
            log.debug('预期结果:{}'.format(expected))
            log.debug('实际结果:{}'.format(res))

            self.excel.write_data(row=row,column=8,value='fail')

            raise e
        else:
            # log.info('用例--{}--执行通过'.format(case['title']))
            self.excel.write_data(row=row, column=8, value='pass')

    @classmethod
    def random_phone(cls):
        '''生成一个数据库里未注册的手机号码'''

        while True:
            phone = '137'
            for i in range(8):
                r = random.randint(0, 9)
                phone += str(r)
            sql = 'select * from futureloan.member where mobile_phone={};'.format(phone)
            res = cls.db.find_count(sql)
            if res == 0:
                return phone