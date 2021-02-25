#!/usr/bin/env python

import sys
import time

from pexpect import pxssh
from log import Logrecord

def handle(ip, username, passwd, sshport, listenport):
    L = Logrecord(ip)
    flag = 1
    #time.sleep(60)
    while 1:
        try:
            s = pxssh.pxssh()
            s.login(ip, username, passwd, port=sshport)
            s.sendline('ps -ef  |grep orcl | grep -v grep')
            s.prompt(timeout=None)
            orcl_inst = s.before.strip().split('\n')[1]
            print orcl_inst
            s.logout()
            break
        except Exception, e:
            print str(e)
            time.sleep(3)
            flag += 1
            if flag > 3:
                orcl_inst = ''
                L.error('network error(ps -ef  |grep orcl | grep -v grep)')
                break

    flag = 1
    while 1:
        try:
            s = pxssh.pxssh()
            s.login(ip, username, passwd, port=sshport)
            s.sendline('netstat -antp | grep %s' % listenport)
            s.prompt()
            listenp = s.before.strip().split('\n')[1:]
            print listenp
            if not 'LISTEN' in str(listenp):
                listenp = ''
            s.logout()
            break
        except Exception ,e:
            print str(e)
            time.sleep(3)
            flag += 1
            if flag > 3:
                listenp = ''
                L.error('netstat -antp | grep %s' % listenport)
                break


    if orcl_inst:
        L.info('oracle install successfully')
    else:
        L.error('oracle install fail')

    if listenp :
        L.info('oracle start successfully')
    else:
        L.error('oracle start fail')


if __name__ == '__main__':
    handle(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
