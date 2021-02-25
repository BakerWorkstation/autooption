#!/usr/bin/env python

import sys
import time

from pexpect import pxssh
from log import Logrecord
from prase import prase_config
from exec_cmd import ssh2

def handle(ip, username, passwd, port):
    webport = prase_config('database', 'webport')
    L = Logrecord(ip)

    flag = 1
    while 1:
        try:
            cmd = ['netstat -antp | grep %s' % webport]
            service = ssh2(ip, port, username, passwd, cmd)[0]
            break
        except Exception:
            time.sleep(3)
            flag += 1
            if flag > 3:
                service = ''
                break
    if service:
        L.info('openfire start successfully')
    else:
        L.error('openfire start fail')


if __name__ == '__main__':
    handle(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
