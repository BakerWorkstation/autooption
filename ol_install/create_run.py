#!/usr/bin/env python

import os
import json
import time
import shutil
import tarfile

import pexpect
import beanstalkc
from pexpect import pxssh

from log import Logrecord
from prase import prase_config


class distribute(object):

    def __init__(self, ip, user, passwd, sshport):
        
        self.ip = ip
        self.username = user
        self.passwd = passwd
        self.sshport = sshport
        self.__L = Logrecord(self.ip)

    def issued(self):

        cmd = 'scp -P %s -r remote_install/autooracle/ %s@%s:/tmp/' %\
 (self.sshport, self.username, self.ip)
        child = pexpect.spawn(cmd)
        child.expect ('(yes/no)? ', timeout=None)
        child.sendline('yes')
        child.expect ('password:', timeout=None)
        child.sendline(self.passwd)
        child.interact()
        child.close()

        cmd1 = 'scp -P %s ./oracle.cfg %s@%s:/tmp/autooracle/' %\
 (self.sshport, self.username, self.ip)
        child = pexpect.spawn(cmd1)
        child.expect ('password:', timeout=None)
        child.sendline(self.passwd)

        child.interact()
        child.close()

        #----------------------------------------

def main():
    # data  from DB.
    # pass    
    for eachlog in os.listdir('./remote_install/logs/'):
        os.remove('./remote_install/logs/%s' % eachlog)

    beanstalk = beanstalkc.Connection(
                                        host = '127.0.0.1',
                                        port = 11300,
                                        parse_yaml = lambda x: x.split('\n')
                                     )
    beanstalk.use('default')
    beanstalk.ignore('oracle')
    beanstalk.use('oracle')

    iplist = prase_config('oracle', 'or_hostip').strip().split(' ')
    while '' in iplist:
        iplist.remove('')
    
    username = prase_config('oracle', 'or_hostusername')
    passwd = prase_config('oracle', 'or_hostpassword')
    sshport = prase_config('oracle', 'or_hostsshport')

    # -- for ---
    try:
        ff = open('/root/.ssh/known_hosts', 'w')
        ff.close()
    except IOError:
        pass

    for eachip in iplist:
        eachip = eachip.strip()
        D = distribute(eachip, username, passwd, sshport)
        D.issued()
        tempdata = {'ip': eachip }
        beanstalk.put(
                       json.dumps(tempdata),
                       delay = 1,
                       priority = 1024
                     )
    # --- for end ---

    beanstalk.put(
                   'end',
                   delay = 1,
                   priority = 1024
                 )

if __name__ == '__main__':
    main()
