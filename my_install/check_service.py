#!/usr/bin/env python

import sys
import time

from pexpect import pxssh
from log import Logrecord


def handle(ip, username, passwd, sshport):
    L = Logrecord(ip)
    flag = 1
    count = 1
    while 1:
        try:
            s = pxssh.pxssh()
            s.login(ip, username, passwd, port=sshport)
            s.sendline('service mysql status')
            s.prompt(timeout=None)
            data = s.before.strip().split('\n')[1]
            print data
            s.logout()
            break
        except Exception, e:
            print str(e)
            time.sleep(3)
            flag += 1
            if flag > 3:
                mysql_inst = ''
                L.error('network error(service mysql status)')
                break


    if data:
        L.info('mysql install successfully')
    else:
        L.error('mysql install fail')


if __name__ == '__main__':
    handle(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
