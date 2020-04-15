''' 
author:紫夏
Time:2020/3/29 16:53
'''
'''
mysql数据库中的utf8和utf-8的区别：
    MySQL中的“utf8”编码只支持最大3字节每字符。
    真正的大家正在使用的UTF-8编码是应该能支持4字节每个字符。 
    目前只能使用utf8,输入utf-8会报错

避免同一个游标：每次查询前新建一个游标或提交一下事务；
    事务具有隔离性，每一个事务之间的操作互不可见
'''


import pymysql
from common.handler_config import conf

class HandlerMysql():
    def __init__(self):
        '''初始化方法中，连接到数据库'''
        # 建立连接
        self.con = pymysql.connect(
            host=conf.get('mysql','host'),
            port=conf.getint('mysql','port'),  # 端口是数值，不是字符创
            user=conf.get('mysql','user'),
            password=conf.get('mysql','password'),
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor  # 定义游标类型，默认为元组类型，改为返回数据为字典
        )
        # 创建一个游标对象
        self.cur=self.con.cursor()

    def find_all(self,sql):
        '''
        查询sql语句，返回所有数据
        :param sql: 查询的sql语句
        :return: 查询到的所有数据
        '''
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_one(self,sql):
        '''
        查询sql语句，返回第一条数据
        :param sql:查询的sql语句
        :type sql:str
        :return:第一条数据
        '''
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def update(self,sql):
        '''
        增删改的操作方法
        :param sql: 增删改的语句
        :return:
        '''
        self.con.commit()
        self.cur.execute(sql)
        self.con.commit()

    def find_count(self,sql):
        '''
            查询sql语句，查询到的数据条数
            :param sql:查询的sql语句
            :return:查询到的数据条数
        '''
        self.con.commit()
        res=self.cur.execute(sql)
        return res


    def close(self):
        '''断开游标，关闭连接（避免占用资源）'''
        self.con.close()
        self.cur.close()


if __name__ == '__main__':

    db=HandlerMysql()
    res=db.find_one('select * from futureloan.member where mobile_phone="15512345005"')
    print(res)