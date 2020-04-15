''' 
author:紫夏
Time:2020/3/19 1:50
'''

from configparser import ConfigParser
from common.handler_path import CONF_DIR
import os

class HandlerConfig(ConfigParser):
    # 父类的父类有init方法,重写Init方法
    def __init__(self,filename):
        super().__init__()
        self.read(filename,encoding='utf8')

conf=HandlerConfig(os.path.join(CONF_DIR,'config.ini'))