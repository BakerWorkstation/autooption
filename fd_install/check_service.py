#!/usr/bin/env python

import sys
import time

from pexpect import pxssh
from log import Logrecord
from prase import prase_config
from exec_cmd import ssh2

def handle(ip, username, passwd, port):
    trackerport = prase_config('fastdfs', 'tracker_port')
    storageport = prase_config('fastdfs', 'storage_port')
    L = Logrecord(ip)
    flag = 1
    while 1:
        try:
            cmd = ['netstat -antp | grep %s' % trackerport]
            data1 = ssh2(ip, port, username, passwd, cmd)
            if data1:
                break
        except Exception as e:
            time.sleep(3)
            flag += 1
            if flag > 3:
                data1 = ''
                break

    flag = 1
    while 1:
        try:
            cmd = ['netstat -antp | grep %s' % storageport]
            data2 = ssh2(ip, port, username, passwd, cmd)[0]
            break
        except Exception:
            time.sleep(3)
            flag += 1
            if flag > 3:
                data2 = ''
                break


    if data1:
        L.info('trackerServer start successfully')
    else:
        L.error('trackerServer start fail')

    if data2:
        L.info('storageServer start successfully')
    else:
        L.error('storageServer start fail')


if __name__ == '__main__':
    handle(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
