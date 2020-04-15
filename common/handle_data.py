

''' 
author:紫夏
Time:2020/4/4 23:53
'''
import re
from common.handler_config import conf
data='{"user": #user#,"pwd": #pwd#,"name": #name#,"age": #age#}'

class EnvData:
    '''定义一个类用来保存用例执行过程中提取出来的数据（当成环境变量的属性）'''
    pass




def replace_data(data):
    '''
    替换数据
    :param data:
    :return:
    '''
    while re.search('#(.*?)#',data):
        res=re.search('#(.*?)#',data)
        key=res.group()

        item=res.group(1)
        try:
            # 获取配置文件中对应的值
            value = conf.get('test_data', item)
        except:
            # 去EnvData类里面获取对应的属性（环境变量）
            value=getattr(EnvData,item)

        data=data.replace(key,value)
    return data

# res=replace_data(data)
# print(res)


