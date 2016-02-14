#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------
# DPE-JS (Javascript based data processing engine)
#
# Copyright(c) Aixi Wang 2014-2015
#--------------------------------------------------
# v01 -- initial version
#--------------------------------------------------
__author__ = "aixi.wang@hotmail.com"
__version__ = "0.3"

import sys
import logging
import time
import os
import thread
import sys
from json import JSONDecoder, JSONEncoder
import json

import PyV8
from utils import *
sys.path.append('../')
from pyiotlib import *

mqttc = None

import sys,time

try:
    import paho.mqtt.client as mqtt
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.client"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt


encoder = JSONEncoder()
decoder = JSONDecoder()

reload(sys)
sys.setdefaultencoding('utf-8')

js_code = ''

#mc = memcache.Client(['127.0.0.1:11211'],debug=False)
#q_rt_data = memcacheq.connect('q_rt_data')

import Queue
mqtt_in_queue = Queue.Queue()
mqtt_out_queue = Queue.Queue()

LOGFILE = 'mqtt_datajs.log.txt'

#-------------------
# log_dump
#-------------------
def log_dump(filename,content):
    if os.name == "nt":
        fpath = '.\\filesystem\\log\\' + filename
    else:
        fpath = './filesystem/log/' + filename
        
    f = file(fpath,'ab')
    t_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    fs = f.write(t_s + '->' + str(content) + '\r\n')
    f.close()
    return
    
#-------------------
# readfile
#-------------------
def readfile(filename):
    f = file(filename,'rb')
    fs = f.read()
    f.close()
    return fs

#-------------------
# js_event_handler 
#-------------------
def js_event_handler(js_code):
    with PyV8.JSContext(CommonJsEnv()) as ctxt:
        ctxt.eval(js_code)
        #print('js_event_handlr ret_code:' + str(ret_code))

#-------------------
# queue_in_put 
#-------------------
def queue_in_put(s):
    mqtt_in_queue.put(s)

#-------------------
# queue_in_get 
#-------------------
def queue_in_get(t):
    try:
        return mqtt_in_queue.get(timeout=t)
    except:
        return ''
#-------------------
# queue_out_put 
#-------------------
def queue_out_put(s):
    mqtt_out_queue.put(s)

#-------------------
# queue_out_get 
#-------------------
def queue_out_get(t):
    try:
        return mqtt_out_queue.get(timeout=t)
    except:
        return ''

#-------------------
# CommonJsEnv 
#-------------------
class CommonJsEnv(PyV8.JSClass):
    def __init__(self, parent=None):
        PyV8.JSClass.__init__(self)

        self.parent = parent
        self.exports = {}
        self.debug = True

    #--------------------------------------------------------------------------------
    #                         Functions for JS calling (start)
    #--------------------------------------------------------------------------------                    
        
    #----------------------
    # require
    #----------------------    
    def require(self, name):
        logging.info("loading module <%s>...", name)
        env = CommonJsEnv(self)
        if name[0] != '.' and name[0] != '/' and len(name) <= 32:
            with open(name + '.js', 'r') as f:
                with PyV8.JSContext(env) as ctxt:
                    ctxt.eval(f.read())
                    return ctxt.locals.exports
                    
    #----------------------
    # sleep
    #----------------------                    
    def sleep(self, t):
        time.sleep(float(t))

    #----------------------
    # puts
    #----------------------                    
    def puts(self, s):
        print s
 
    #----------------------
    # dbg
    #----------------------                    
    def dbg(self, s):
        if self.debug == True:
            print s

    #----------------------
    # queue_in_get
    #----------------------                    
    def queue_in_get(self,t):
        return queue_in_get(t)

    #----------------------
    # queue_out_put
    #----------------------                    
    def queue_out_put(self,s):
        return queue_out_put(s)

    #----------------------
    # disable_dbg 
    #----------------------                    
    def disable_dbg(self):
        self.debug = False

    #----------------------
    # enable_dbg 
    #----------------------                    
    def enable_dbg(self):
        self.debug = True
 
    #----------------------
    # sendmail
    #----------------------                    
    def sendmail(self, s1, s2, s3):
        return mysendmail(s1,s2,s3)
 
    #----------------------
    # now
    #----------------------  
    def now(self):
        return time.time()
 
    #----------------------
    # format_time
    #----------------------  
    def format_time(self,t):
        return format_time_from_linuxtime(t)
        
    #----------------------
    # get_raw_data
    #----------------------      
    def get_raw_data(self,p,t1,t2):
        s1 = str(p)
        s2 = str(t1)
        s3 = str(t2)     
        return get_raw_data(s1,s2,s3)

    #----------------------
    # get_stats_data
    #----------------------      
    def get_stats_data(self,p,t1,t2):
        s1 = str(p)
        s2 = str(t1)
        s3 = str(t2)    
        return get_stats_data(s1,s2,s3)        
        
    #----------------------
    # get_alarms_data
    #----------------------      
    def get_alarms_data(self,p,t1,t2):
        s1 = str(p)
        s2 = str(t1)
        s3 = str(t2)
        #print 'in=>',s1,s2,s3
        return get_alarms_data(s1,s2,s3) 
 
    #----------------------
    # save_log
    #---------------------- 
    def save_log(self,name,data):
        s = str(data)
        return save_log(name,s)

    #----------------------
    # log_dump
    #----------------------        
    def log_dump(self,content):
        log_dump(LOGFILE,content)
        
    #----------------------
    # save_stats
    #---------------------- 
    def save_stats(self,name,time,data):
        s1 = str(name)
        s2 = str(time)
        s3 = str(data)
        return save_stats(s1,s2,s3)

    #----------------------
    # save_alarm
    #---------------------- 
    def save_alarm(self,name,data):
        s1 = str(name)
        #s2 = str(time)
        s3 = str(data)
        return save_alarm(s1,s3)

    #----------------------
    # save_alarm2
    #---------------------- 
    def save_alarm2(self,name,data,time):
        s1 = str(name)
        s2 = str(data)
        s3 = str(time)
        return save_alarm2(s1,s2,s3)

    #-----------------------
    # save2cache
    #-----------------------
    def save2cache(self,s):
        #print 'from rpc_server.save2cache' + s
        #mc.set('sandboxc_status',str(s),60)
        pass
    #-----------------------
    # append2cache
    #-----------------------
    def append2cache(self,s):
        #print 'from rpc_server.save2cache' + s
        #s2 = str(mc.get('sandboxc_status')) + '<br>' + str(s)
        #mc.set('sandboxc_status',s2,60)
        pass
    #-----------------------
    # pop_rt_data
    #-----------------------    
    def pop_rt_data(self):
        try:
            s = q_rt_data.get()
            if s == None:
                return ''
            else:
                return s
        except:
            return ''

    #-----------------------
    # mqtt_subscribe
    #-----------------------            
    def mqtt_subscribe(self,topic,qos):
        global mqttc
        mqttc.subscribe(topic,qos)
        
    #-----------------------
    # mqtt_unsubscribe
    #-----------------------            
    def mqtt_unsubscribe(self,topic):
        global mqttc
        mqttc.unsubscribe(topic)
        
    #-----------------------
    # db_set_kv
    #-----------------------
    def db_set_kv(self,k,v):
        s1 = str(k)
        s2 = str(v)
        return db_set_kv(s1,s2)

    #-----------------------
    # db_get_kv
    #-----------------------
    def db_get_kv(self,k):
        s1 = str(k)
        return db_get_kv(s1)

        
    #-----------------------
    # hex2str
    #-----------------------
    def hex2str(self,h):
        s = h.decode('hex')
        return s

    #-----------------------
    # str2hex
    #-----------------------
    def str2hex(self,s):
        h = s.encode('hex')
        return h

    #-----------------------
    # str2hex
    #-----------------------
    def str2hex(self,s):
        h = s.encode('hex')
        return h
        
    #--------------------------------
    # get misc. info from linux time
    #--------------------------------        
    def get_hour_from_linuxtime(self,t):
        return get_hour_from_linuxtime(t)
    def get_min_from_linuxtime(self,t):
        return get_min_from_linuxtime(t)
    def get_mday_from_linuxtime(self,t):
        return get_mday_from_linuxtime(t)
    def get_yday_from_linuxtime(self,t):
        return get_yday_from_linuxtime(t)
    def get_wday_from_linuxtime(self,t):
        return get_wday_from_linuxtime(t)
    def get_mon_from_linuxtime(self,t):
        return get_mon_from_linuxtime(t)
    def get_year_from_linuxtime(self,t):
        return get_year_from_linuxtime(t)

    #--------------------------------------------------------------------------------
    #                         Functions for JS calling (end)
    #--------------------------------------------------------------------------------                    
    @staticmethod
    def execute(script):
        logging.info("executing script...")

        env = CommonJsEnv()

        with PyV8.JSContext(env) as ctxt:
            return ctxt.eval(script)

#---------------------------------
# MQTT on_xxx hooks
#---------------------------------

def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    json_s1 = {}
    json_s1['topic'] = msg.topic
    json_s1['payload'] = msg.payload
    json_s1['ts'] = float(time.time())
    json_s2 = json.dumps(json_s1)
    print('json_s2:'+str(json_s2))
    queue_in_put(json_s2)
    #js_event_handler(js_code)
    
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

#---------------------------------
# main
#---------------------------------

if __name__=='__main__':
    log_dump(LOGFILE, 'mqtt_datajs started 1')
    pid = os.getpid()
    writefile('mqtt_datajs.pid',str(pid))

    if os.name == "nt":
        filename = sys.path[0] + '\\p.js'
    else:
        filename = sys.path[0] + '/p.js'
    
    js_code = readfile(filename)
    #print 'js_code:',js_code
    log_dump(LOGFILE, 'mqtt_datajs started')
    
    #js_code = "function event_handler(s1,s2) { return 'hello ' + s1 + s2; };"
    firstPy = PyV8.JSExtension("event_handler", js_code, register=False)
    firstPy.register()
    print('read js code done from file ' + filename + ' event_handler registered')
    #js_event_handler(js_code)
               
    # mqttc = mqtt.Client("client-id")
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    #mqttc.on_log = on_log
    #mqttc.username_pw_set('data', 'data')

    mqttc.connect("test.mosquitto.org", 1883, 60)
    #mqttc.connect("127.0.0.1", 1883, 60)

    #mqttc.subscribe("home/#", 2)

    #mqttc.loop_forever()
    mqttc.loop_start()
    while True:
    	js_event_handler(js_code)
        time.sleep(30)
        print 'sleep...'
