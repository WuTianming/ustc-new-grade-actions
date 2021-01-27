#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

# login
username = os.environ['CAS_USERNAME']
password = os.environ['CAS_PASSWD']

# sender_email
mail_host = os.environ['MAIL_HOST']
mail_user = os.environ['MAIL_SENDER']
mail_passwd = os.environ['MAIL_PASSWD']
use_ssl = True
ssl_port = 465

# receiver_email
receivers = ['2300281344@qq.com','wutianming@mail.ustc.edu.cn']
