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


global L
L = []

class DaemonP(threading.Thread):

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
 
    def run(self):
        handle(self.ip)
        

def handle(ip):
    username = prase_config('mysql', 'my_hostusername')
    passwd = prase_config('mysql', 'my_hostpassword')
    sshport = prase_config('mysql', 'my_hostsshport')
    
    R = Logrecord(ip)    

    flag = 1
    while 1:
        try:
            s = pxssh.pxssh()
            s.login(ip, username, passwd, port=sshport)
            s.sendline('cd /tmp/automysql && python mysqlinstall.py')
            s.prompt(timeout=None)
            tempdata = s.before
            s.sendline('cd /tmp/automysql && python mysqlconf.py')
            s.prompt(timeout=None)
            tempdata += s.before
            s.logout()
            break
        except Exception, e:
            print str(e)
            time.sleep(3)
            flag += 1
            if flag > 3:
                R.error('network error(python *.py)')
                break
    data = tempdata.split('\n')[1:]
    for line in data:
        R.info(line.strip())

    # ------wait cluster ------ #

    A = subprocess.Popen('python ./check_service.py %s %s %s %s' %\
 (ip, username, passwd, sshport), shell=True)
    A.wait()

if __name__ == '__main__':
    beanstalk = beanstalkc.Connection(
                                        host = '127.0.0.1',
                                        port = 11300,
                                        parse_yaml = lambda x: x.split('\n')
                                     )

    beanstalk.watch('mysql')

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
