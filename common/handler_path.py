''' 
author:紫夏
Time:2020/3/29 2:03
'''

import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# print(BASE_DIR)

# 用例模块所在目录
CASE_DIR=os.path.join(BASE_DIR,'testcases')
# 用例数据所在目录
DATA_DIR=os.path.join(BASE_DIR,'data')
# 配置文件所在目录
CONF_DIR=os.path.join(BASE_DIR,'conf')
# 测试报告所在目录
REPORT_DIR=os.path.join(BASE_DIR,'report')
# 日志所在目录
LOG_DIR=os.path.join(BASE_DIR,'logs')


# 用例数据所在路径
casefilename=os.path.join(DATA_DIR,'cases.xlsx')



