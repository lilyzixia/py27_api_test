''' 
author:紫夏
Time:2020/4/15 0:44
'''


import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from common.handler_path import REPORT_DIR
import os

def send_msg():
    # 1.1连接smtp服务器，并登陆
    smtp = smtplib.SMTP_SSL(host='smtp.qq.com', port=465)
    # 1.2并登陆 用邮箱账号和授权码登录，不是邮箱的密码
    smtp.login(user='709737032@qq.com', password='lcprngsxqrmxbehi')

    # 2.构造一封多组件的邮件
    msg = MIMEMultipart()
    msg['Subject'] = '上课邮件001'
    msg['To'] = '1711179415@qq.com'
    msg['From'] = '709737032@qq.com'

    # 构建邮件的文本内容
    text = MIMEText('邮件中的文本内容', _charset='utf-8')
    msg.attach(text)

    # 报告名不写死
    with open(os.path.join(REPORT_DIR,'report.html'), 'rb') as f:
        content = f.read()
    # 构造邮件的附件
    report = MIMEApplication(content)
    # 可以设置filename,邮件显示的文件名字
    report.add_header('content-disposition', 'attachment', filename='python.html')
    msg.attach(report)

    # 3发送邮件
    smtp.send_message(msg, from_addr='709737032@qq.com', to_addrs='1711179415@qq.com')




