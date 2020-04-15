''' 
author:紫夏
Time:2020/3/7
'''

# import unittest
# from BeautifulReport import BeautifulReport
#
# suite=unittest.defaultTestLoader.discover(r'F:\python37test\py27\day17\HOMEWORK')
# br =BeautifulReport(suite)
# br.report('py27期day17作业','brreport.html')



import HTMLTestRunnerNew
import unittest
from BeautifulReport import  BeautifulReport
from common.Handler_Logging import log
from common.handler_path import CASE_DIR,REPORT_DIR
from common.send_email import send_msg

log.info('-------------------开始执行测试用例---------------------')

# 创建测试套件
suite=unittest.TestSuite()
loader=unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))
# br=BeautifulReport(suite)
#
# br.report('接口测试',filename='report.html',report_dir=REPORT_DIR)
runner=HTMLTestRunnerNew(stream=open('new_report.html','wb'),
                      title='27期第一份测试报告',
                      tester='lisa',
                      description='第一个版本的测试'
                      )
runner.run(suite)

log.info('-------------------测试用例执行完毕---------------------')


send_msg()

# html_TestRunnerNew

#



