#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
class Log(object):
    def __init__(self,name=None,log_path='./running.log'):
        self.logger=logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.log_path=log_path
        # write to file
        fh=logging.FileHandler(self.log_path,'a',encoding='utf-8')
        fh.setLevel(logging.INFO)
        #format
        fmt='%(asctime)s %(message)s'
        datefmt='%Y/%m/%d %H:%M:%S %p'
        formatter=logging.Formatter(fmt,datefmt)
        fh.setFormatter(formatter)
        #write to console
        ch=logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        #add handlers
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    def getlog(self):
        return self.logger