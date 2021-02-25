#!/usr/bin/env python

import sys
import time

from pexpect import pxssh
from log import Logrecord

def handle(ip, username, passwd, sshport, role, webport, listenport):
    L = Logrecord(ip)
    flag = 1
    while 1:
        try:
            s = pxssh.pxssh()
            s.login(ip, username, passwd, port=sshport)
            s.sendline('ls /app/weblogic/Oracle/Middleware/wlserver_10.3')
            s.prompt(timeout=None)
            install_dir = s.before.strip().split('\n')[1]
            s.logout()
            break
        except Exception:
            time.sleep(3)
            flag += 1
            if flag > 3:
                install_dir = ''
                L.error('network error(ls /app/weblogic/Oracle/Middleware/wlserver_10.3)')
                break

    flag = 1
    time.sleep(40)
    while 1:
        try:
            s = pxssh.pxssh()
            s.login(ip, username, passwd, port=sshport)
            s.sendline('netstat -antp | grep %s' % listenport)
            s.prompt()
            listenp = s.before.strip().split('\n')[1]
            if not 'LISTEN' in listenp:
                listenp = ''
            if role == 'admin':
                s.sendline('netstat -antp | grep %s' % webport)
                s.prompt()
                webp = s.before.strip().split('\n')[1]
                if not 'LISTEN' in webp:
                    webp = ''
            s.logout()
            break
        except Exception as e:
            time.sleep(3)
            flag += 1
            if flag > 3:
                listenp = ''
                webp = ''
                break


    if install_dir:
        L.info('weblogic install successfully')
    else:
        L.error('weblogic install fail')

    if role == 'admin':
        if webp and listenp :
            L.info('weblogic start successfully')
        else:
            L.error('weblogic start fail')
    elif role == 'common':
        if listenp:
            L.info('weblogic start successfully')
        else:
            L.error('weblogic start fail')


if __name__ == '__main__':
    handle(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
