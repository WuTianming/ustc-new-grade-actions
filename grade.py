#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import io
import re
import sys
import time
import pickle
import requests
from log import Log
from mail import send_email
from config import username,password
import PIL
import pytesseract
from selenium import webdriver
from PIL import Image
import json
import datetime
import pytz
import argparse
from bs4 import BeautifulSoup


logger=Log(__name__).getlog()

CAS_RETURN_URL = "https://jw.ustc.edu.cn/caslogin"
url1='https://passport.ustc.edu.cn/login?service=https://jw.ustc.edu.cn/ucas-sso/login'
url2='https://jw.ustc.edu.cn/ucas-sso/login'
url3='https://jw.ustc.edu.cn/for-std/grade/sheet/getSemesters'
headers={
    'Connection': 'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
pattern1=re.compile("\"id\":(.+?),")
pattern2=re.compile("{(.+?)}")
pattern3=re.compile("\"courseNameCh\":\"(.+?)\",")
pattern4=re.compile("\"score\":\"(.+?)\",")

def login(s):
    url = "https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin"
    r = s.get(url, params={"service": CAS_RETURN_URL})
    x = re.search(r"""<input.*?name="CAS_LT".*?>""", r.text).group(0)
    cas_lt = re.search(r'value="(LT-\w*)"', x).group(1)
    print("cas_lt")
    print(cas_lt)

    logger.info('logging in...')
    CAS_CAPTCHA_URL = "https://passport.ustc.edu.cn/validatecode.jsp?type=login"
    r = s.get(CAS_CAPTCHA_URL)
    
    img = PIL.Image.open(io.BytesIO(r.content))
    pix = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pix[i, j]
            if g >= 40 and r < 80:
                pix[i, j] = (0, 0, 0)
            else:
                pix[i, j] = (255, 255, 255)
    lt_code = pytesseract.image_to_string(img).strip()   
    print("lt_code")
    print(lt_code) 

    data = {
        'model':'uplogin.jsp',
        'CAS_LT':cas_lt,
        'service':'https://jw.ustc.edu.cn/ucas-sso/login',
        'warn':'',
        'showCode':'',
        'username':username,
        'password':password,
        'button':'',
        'LT': lt_code
    }
    r1=s.post(url1,data=data,headers=headers)
    if not '教务系统' in r1.text:
        logger.info('username or password wrong!')
        sys.exit(1)
    s.get(url2,headers=headers)
    logger.info('login complete!')

def get_ID(s):
    logger.info('getting semester id...')
    getid=s.get(url3,headers=headers)
    IDs=getid.text
    IDs=re.findall(pattern1,IDs)
    IDs=list(map(int,IDs))
    max_ID=max(IDs)
    return max_ID

def get_grade(s,max_ID):
    logger.info('getting the grades...')
    url4='https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeList?trainTypeId=1&semesterIds=' + str(max_ID)
    Grades=s.get(url4,headers=headers).text
    if '统一身份认证登录' in Grades:
        logger.info('Not logged in, retry by recursion...')
        login(s)
        return get_grade(s,max_ID)
    sheet=re.findall(pattern2,Grades)
    return sheet

def parse_grade(sheet):
    grades=[]
    for i in range(1,len(sheet)-1):
        courseName=re.findall(pattern3,sheet[i])
        courseName=courseName[0]
        score=re.findall(pattern4,sheet[i])
        score=int(score[0])
        grades.append((courseName,score))
    return grades

grade_len=0
grades_key=[]
max_ID=0
first_access=True
if ("sync" in sys.argv):
    email=False
    logger.info("Syncing data from server, no email will be sent even if there are new grades present")
else:
    email=True

logger.info("Started")

if os.path.exists('grades_key.pickle') and os.path.getsize('grades_key.pickle'):
    logger.info('Find the old data, reading...')
    f=open('grades_key.pickle','rb')
    grades_key=pickle.load(f)
    grade_len=len(grades_key)
    f.close()

s=requests.Session()


logger.info('Query...')
if(first_access):
    login(s)
    max_ID=get_ID(s)
    first_access=False
    
print("first_access")

sheet=get_grade(s,max_ID)


if(len(sheet)==grade_len+1): # no new grade
    logger.info('no new grades')
else:
    f=open('grades_key.pickle','wb')
    print("open")
    new_grades=parse_grade(sheet)
    new_grade_key=list(set([k for k,v in new_grades]) - set(grades_key))
    new_grade = []
    logger.info("* new grades fetched!")
    for k,v in new_grades:
        if k in new_grade_key:
            new_grade.append((k,v))
            logger.info(k)
    grades_key = [k for k,v in new_grades]
    grade_len=len(new_grades)
    logger.info('writing key to file...')
    pickle.dump(grades_key,f)
    f.close()
    if (email):
        logger.info('sending Email...')
        send_email(new_grade)
