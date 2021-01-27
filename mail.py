#!/usr/bin/python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from log import Log
from config import mail_host,mail_user,mail_passwd,use_ssl,ssl_port,receivers

def send_email(new_grade):
    logger=Log(__name__).getlog()
    try:
        if(mail_host=='' or mail_user=='' or mail_passwd == ''):
            raise Exception('Please input sender information!!!')
        if(receivers ==[]):
            raise Exception('Please input receiver information!!!')
    except Exception as e:
        logger.info('Exception: '+str(e))
        return
    if use_ssl:
        ssl_address=mail_host+':'+str(ssl_port)
    grade_len=len(new_grade)
    text='新成绩：\n'
    for i in range(grade_len):
        text+=str(new_grade[i][0])+' : '+str(new_grade[i][1])+'\n'
    message = MIMEText(text,'plain','utf-8')
    subject = '您有新成绩！'
    message['Subject']=Header(subject,'utf-8')
    message['From']=Header(mail_user,'utf-8')
    message['To']=Header(",".join(receivers),'utf-8')
    try:
        if use_ssl:
            smtp=smtplib.SMTP_SSL(ssl_address)
        else:
            smtp=smtplib.SMTP()
            smtp.connect(mail_host,25)
        smtp.login(mail_user,mail_passwd)
        smtp.sendmail(mail_user,receivers,message.as_string())
        smtp.quit()
    except smtplib.SMTPException:
        logger.info("Error: 无法发送邮件")
        return
    logger.info('Email has been sent successfully!')
