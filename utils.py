#!/usr/bin/python
#-*- coding: utf-8 -*-
#---------------------------------------
# Common Routines
#
# Copyright(c) Aixi Wang 2014-2015
#---------------------------------------
# v1 -- initial version
#---------------------------------------
import time
import random
import json
import sys
import logging
import os
import thread
from json import JSONDecoder, JSONEncoder

import PyV8
from utils import *
sys.path.append('../')
from pyiotlib import *

encoder = JSONEncoder()
decoder = JSONDecoder()

reload(sys)
sys.setdefaultencoding('utf-8')
from global_setting import *


#-----------------------------
# mysendmail 
#
# p1: receiver
# p2: subject
# p3: content
#-----------------------------
def mysendmail(p1,p2,p3):
    try:
        global mail_enable
        global mail_sender,mail_smtpserver,mail_username,mail_password
        import sys,os
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header
        sender = mail_sender
        smtpserver = mail_smtpserver
        username = mail_username
        password = mail_password
        
        if (mail_enable == 0):
            return
        receiver=p1
        subject = p2
        if (len(p3) > 0):
            msg = MIMEText(p3,'plain','utf-8')
        else:
            msg = MIMEText('..','plain','utf-8')
        msg['Subject'] = Header(subject, 'utf-8')

        # prepare attachment
        #att = MIMEText(open('h:\\python\\1.jpg', 'rb').read(), 'base64', 'utf-8')
        #att["Content-Type"] = 'application/octet-stream'
        #att["Content-Disposition"] = 'attachment; filename="1.jpg"'
        #msg.attach(att)

        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()

        return 0
    except:
        return -1

#-------------------
# get_raw_data
#-------------------
def get_raw_data(p,t1,t2):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.get_datas(p,t1,t2)
        
        if json_out['code'] == 0:   
            arr = []
            for record in json_out['data']:
                k = record[0]
                v = record[1]
                s = k.split(':')       
                res =  {
                    'p': s[1],
                    't': s[2],
                    'v': v
                }        
                arr.append(res)

            res2 = {
                'code': 0,
                'data': arr,
            }
        else:
            res2 = {
                'code': -1,
                'data': 'error',
            }
        
        #return encoder.encode(res2)
        return res2
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        
        #return encoder.encode(res2)
        return res2        

#-------------------
# get_stats_data
#-------------------
def get_stats_data(p,t1,t2):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.get_stats(p,t1,t2)
        
        if json_out['code'] == 0:   
            arr = []
            for record in json_out['data']:
                k = record[0]
                v = record[1]
                s = k.split(':')       
                res =  {
                    'p': s[1],
                    't': s[2],
                    'v': v
                }        
                arr.append(res)

            res2 = {
                'code': 0,
                'data': arr,
            }
        else:
            res2 = {
                'code': -1,
                'data': 'error',
            }
        
        #return encoder.encode(res2)
        return res2
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        
        #return encoder.encode(res2)
        return res2

#-------------------
# get_alarms_data
#-------------------
def get_alarms_data(p,t1,t2):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.get_alarms(p,t1,t2)
        if json_out['code'] == 0:   
            arr = []
            for record in json_out['data']:
                k = record[0]
                v = record[1]
                s = k.split(':')       
                res =  {
                    'p': s[1],
                    't': s[2],
                    'v': v
                }        
                arr.append(res)

            res2 = {
                'code': 0,
                'data': arr,
            }
        else:
            res2 = {
                'code': -1,
                'data': 'error',
            }
        
        #return encoder.encode(res2)
        return res2
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        
        #return encoder.encode(res2)
        return res2 

#-------------------
# save_log
#-------------------
def save_log(name,dat):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.save_log(name,dat)        
        if json_out['code'] == 0: 
            res2 = {
                'code': 0,
                'data': 'ok',
            }        
        else:
            res2 = {
                'code': -1,
                'data': 'return fail',
            }        
        return res2
        
        
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        
        #return encoder.encode(res2)
        return res2

#-------------------
# save_alarm
#-------------------
def save_alarm(name,data):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.save_alarm(name,data)        
        if json_out['code'] == 0: 
            res2 = {
                'code': 0,
                'data': 'ok',
            }        
        else:
            res2 = {
                'code': -1,
                'data': 'return fail',
            }        
        return res2
        
        
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        
        #return encoder.encode(res2)
        return res2        
#-------------------
# save_alarm2
#-------------------
def save_alarm2(name,data,time):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.save_alarm(name,data,time)        
        if json_out['code'] == 0: 
            res2 = {
                'code': 0,
                'data': 'ok',
            }        
        else:
            res2 = {
                'code': -1,
                'data': 'return fail',
            }        
        return res2
        
        
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        
        #return encoder.encode(res2)
        return res2

   
#-----------------------
# get_alarms
#-----------------------
def get_alarms(t):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.get_alarms('*',time.time()-t,time.time())
    
        if json_out['code'] == 0:   
            arr = []
            for record in json_out['data']:
                k = record[0]
                v = record[1]
                s = k.split(':')       
                res =  {
                    'name': s[1],
                    'time': format_time_from_linuxtime(s[2]),
                    'type': v
                }
                # latest, first
                arr.append(res)

            res2 = {
                'code': 0,
                'data': arr,
            }
        else:
            res2 = {
                'code': -1,
                'data': 'error',
            }
        
        return res2


    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        return res2
#-----------------------
# save_stats
#-----------------------
def save_stats(p,t,v):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.save_stats(p, t, v)    
        if json_out['code'] == 0:      
            res2 = {
                'code': 0,
                'data': 'ok',
            }
        else:
            res2 = {
                'code': -1,
                'data': 'error',
            }
        
        return res2
        
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        return res2    

    

 
#-----------------------
# db_set_kv
#-----------------------
def db_set_kv(k,v):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.set(k, v)    
        if json_out['code'] == 0:      
            res2 = {
                'code': 0,
                'data': 'ok',
            }
        else:
            res2 = {
                'code': -1,
                'data': 'error',
            }
        
        return res2
        
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        return res2

#-----------------------
# db_get_kv
#-----------------------
def db_get_kv(k):
    try:
        auth_key = readfile('./key.txt')
        rpc = app_sdk(auth_key,server_ip='115.29.178.81',server_port=7777)
        json_out = rpc.get(k)    
        return json_out
        
        
    except:
        res2 = {
            'code': -2,
            'data': 'exception',
        }
        return res2
        
#--------------------------
# get_xxx_linuxtime
#--------------------------
def get_hour_from_linuxtime(t):
    return time.localtime(float(t)).tm_hour
def get_min_from_linuxtime(t):
    return time.localtime(float(t)).tm_min 
def get_sec_from_linuxtime(t):
    return time.localtime(float(t)).tm_sec
def get_mday_from_linuxtime(t):
    return time.localtime(float(t)).tm_mday
def get_yday_from_linuxtime(t):
    return time.localtime(float(t)).tm_yday
def get_wday_from_linuxtime(t):
    return time.localtime(float(t)).tm_wday
def get_mon_from_linuxtime(t):
    return time.localtime(float(t)).tm_month
def get_year_from_linuxtime(t):
    return time.localtime(float(t)).tm_year
def get_isdst_from_linuxtime(t):
    return time.localtime(float(t)).tm_isdst
def format_time_from_linuxtime(t):
    s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t)))
    return s
def get_linuxtime_from_str(s):
    #'10:53:45 2013-10-21'
    struct_time = time.strptime(s,'%H:%M:%S %Y-%m-%d')
    t = time.mktime(struct_time)
    return t

#--------------------------
# power_low_price
#--------------------------    
def power_low_price():
    return 0.3070
    
#--------------------------
# power_high_price
#--------------------------  
def power_high_price():
    return 0.6170

#--------------------------
# get_power_price
#--------------------------
def get_power_price(t):
    h = get_hour_from_linuxtime(t)
    if h >= 6 and h < 22:
        return power_high_price()
    else:
        return power_low_price()

#--------------------------
# caculate_power_cost
#--------------------------
def caculate_power_cost(t1,t2,current):
    #print '>>>'
    #print format_time_from_linuxtime(t1),' ', format_time_from_linuxtime(t2)
    f = (t2-t1)*current*get_power_price(t2)*0.22/3600.0
    #print 'cost is :',f
    return f


 
