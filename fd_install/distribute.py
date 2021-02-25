#!/usr/bin/env python

import os
import time
import json
import threading
import subprocess

import beanstalkc
import pexpect
from pexpect import pxssh

from log import Logrecord
from prase import prase_config
from exec_cmd import ssh2

global L
L = []

class DaemonP(threading.Thread):

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
  
    def run(self):
        handle(self.ip)
        

def handle(ip):
    iplist = prase_config('distribute', 'distip').strip().split(' ')
    while '' in iplist:
        iplist.remove('')

    userlist = prase_config('distribute', 'username').strip().split(' ')
    while '' in userlist:
        userlist.remove('')

    passwdlist = prase_config('distribute', 'password').strip().split(' ')
    while '' in passwdlist:
        passwdlist.remove('')

    portlist = prase_config('distribute', 'hostport').strip().split(' ')
    while '' in portlist:
        portlist.remove('')

    index = iplist.index(ip)
    # username
    try:
        hostusername = userlist[index]
    except:
        hostusername = userlist[0]
    # password
    try:
        hostpassword = passwdlist[index]
    except:
        hostpassword = passwdlist[0]
    # port
    try:
        hostport = portlist[index]
    except:
        hostport = portlist[0]

    R = Logrecord(ip)    
    flag = 1
    while 1:
        try:
            cmd = ['chmod +x /tmp/FastDFS_Install.run', 'cd /tmp/ && ./FastDFS_Install.run']
            data = ssh2(ip, hostport, hostusername, hostpassword, cmd)
            for line in data:
                R.info(line.strip())
            break
        except Exception:
            time.sleep(3)
            flag += 1
            if flag > 3:
                R.error('network error(./*run)')
                break
    while 1:
        try:
            cmd = ['ls /etc/fdfs/storage.conf &> /dev/null ; echo $?']
            info = ssh2(ip, hostport, hostusername, hostpassword, cmd)
            if '0' == info[0].replace('\n', ''):
                R.info('fastdfs install successfully')
                break
        except Exception as e:
            time.sleep(3)

    time.sleep(10)
    A = subprocess.Popen('python ./check_service.py %s %s %s %s' %\
 (ip, hostusername, hostpassword, hostport), shell=True)
    A.wait()

if __name__ == '__main__':
    beanstalk = beanstalkc.Connection(
                                        host = '127.0.0.1',
                                        port = 11300,
                                        parse_yaml = lambda x: x.split('\n')
                                     )

    beanstalk.watch('fastdfs')
    #print 'beanstalk.watching : %s ' %  beanstalk.watching()
    #print 'tubes : %s' % beanstalk.tubes()

    while 1:
        job = beanstalk.reserve(timeout=5)
        try:
            data = job.body
        except AttributeError:
            time.sleep(1)
            continue
    
        if data == 'end':
            job.delete()
            while 1:
                for thread in L:
                    if not thread.isAlive():
                        L.remove(thread)
                if len(L) == 0:
                    os._exit(0)
    
        info = json.loads(data)
        ip = info['ip']
        try:
            P = DaemonP(ip)
            P.setDaemon(True)
            P.start()
            L.append(P)
    
            job.delete()
        except Exception:
            pass
    
    beanstalk.close()
