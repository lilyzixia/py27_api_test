''' 
author:紫夏
Time:2020/3/15 23:34
'''
'''
1、将封装好上课创建日志收集器的函数
2、将之前注册函数用例方法中将执行的结果记录到日志文件中
（通过的用例记录info等级的日志，没通过的用例记录error等级的日志）
'''
import logging
from common.handler_config import conf
import os
from common.handler_path import LOG_DIR




log_filepath=os.path.join(LOG_DIR,conf.get('log','filename'))
def handlerlogging():
    # 创建日志收集器;设置日志收集器等级
    logcollect=logging.getLogger('zixia')
    logcollect.setLevel(conf.get('log','level'))
    # conf.get('log', 'level')

#     创建输出到控制台渠道;控制台等级；控制台添加到日志收集器
    sh=logging.StreamHandler()
    sh.setLevel(conf.get('log','sh_level'))
    logcollect.addHandler(sh)

#     创建输出文件渠道;文件等级；文件添加到日志收集器
    fh = logging.FileHandler(log_filepath,encoding='utf8')
    fh.setLevel(conf.get('log','fh_level'))
    logcollect.addHandler(fh)

    # 设置日志格式
    formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
    format=logging.Formatter(formats)
    sh.setFormatter(format)
    fh.setFormatter(format)

    return logcollect

log=handlerlogging()




