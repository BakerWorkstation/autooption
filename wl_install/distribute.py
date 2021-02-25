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

    def __init__(self, ip, role):
        threading.Thread.__init__(self)
        self.ip = ip
        self.role = role   
 
    def run(self):
        handle(self.ip, self.role)
        

def handle(ip, role):
    iplist = prase_config('weblogic', 'wl_iplist').strip().split(' ')
    while '' in iplist:
        iplist.remove('')

    userlist = prase_config('weblogic', 'wl_hostusername').strip().split(' ')
    while '' in userlist:
        userlist.remove('')

    passwdlist = prase_config('weblogic', 'wl_hostpassword').strip().split(' ')
    while '' in passwdlist:
        passwdlist.remove('')

    portlist = prase_config('weblogic', 'wl_hostsshport').strip().split(' ')
    while '' in portlist:
        portlist.remove('')

    master_ip = prase_config('weblogic', 'wl_adminserver').strip().split(' ')[-1]
    listenport = prase_config('weblogic', 'wl_listenport')
    httpport = prase_config('weblogic', 'wl_httpport')
    usertype = prase_config('weblogic', 'wl_usertype')

    iplist.remove(master_ip)
    iplist.insert(0, master_ip)

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
            s = pxssh.pxssh()
            s.login(ip, hostusername, hostpassword, hostport)
            s.sendline('cd /tmp/autoweblogic && python install_pexpect.py')
            s.prompt(timeout=None)
            tempdata = s.before
            s.sendline('cd /tmp/autoweblogic && python weblogicconf.py')
            s.prompt(timeout=None)
            tempdata += s.before
            s.logout()
            break
        except Exception:
            time.sleep(3)
            flag += 1
            if flag > 3:
                R.error('network error(python *.py)')
                break
 
    
    data = tempdata.split('\n')[1:]
    for line in data:
        R.info(line.strip())

    time.sleep(3)
    while 1:
        try:
            s = pxssh.pxssh()
            s.login(ip, hostusername, hostpassword, hostport)
            s.sendline('ifconfig')
            s.prompt(timeout=None)
            rpminfo = s.before.strip()
            s.logout()
            break
        except Exception, e:
            time.sleep(3)
            print str(e)
            pass
 
    # ------wait cluster ------ #
    flag = 1
    count = 1
    while 1:
        try:
            s = pxssh.pxssh()
            s.login(ip, hostusername, hostpassword, hostport)
            if usertype == 'root':
                s.sendline("/etc/init.d/weblogic start && sleep 30 && /etc/init.d/weblogic start")
            elif usertype == 'weblogic':
                s.sendline("su - weblogic -c 'sleep 10 && /etc/init.d/weblogic start && sleep 30 && /etc/init.d/weblogic start'")
            s.prompt(timeout=None)
            tempdata = s.before
            data = tempdata.split('\n')[1:]
            print data
            s.logout()
            if role == 'admin' and data[-2].find('already started') > 0 and data[-3].find('already started') > 0:
                break
            elif role == 'common' and data[-2].find('already started') > 0:
                break
            count += 1
            if count > 3:
                break
        except Exception, e:
            print str(e)
            time.sleep(3)
            flag += 1
            if flag > 3:
                R.error('network error(start service)')
                break

    A = subprocess.Popen('python ./check_service.py %s %s %s %s %s %s %s' %\
 (ip, hostusername, hostpassword, hostport, role, httpport, listenport), shell=True)
    A.wait()

if __name__ == '__main__':
    beanstalk = beanstalkc.Connection(
                                        host = '127.0.0.1',
                                        port = 11300,
                                        parse_yaml = lambda x: x.split('\n')
                                     )

    beanstalk.watch('weblogic')

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
            role = info['role']
        except Exception:
            role = 'common'

        try:
            P = DaemonP(ip, role)
            P.setDaemon(True)
            P.start()
            L.append(P)
            job.delete()
        except Exception:
            pass
    
    beanstalk.close()
