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

        cmd = 'scp -P %s -r remote_install/autoweblogic/ %s@%s:/tmp/' %\
 (self.sshport, self.username, self.ip)
        child = pexpect.spawn(cmd)
        child.expect ('(yes/no)? ', timeout=None)
        child.sendline('yes')
        child.expect ('password:', timeout=None)
        child.sendline(self.passwd)
        child.interact()
        child.close()

        cmd1 = 'scp -P %s /opt/autooption/autooption/wl_%s.cfg %s@%s:/tmp/autoweblogic/' %\
 (self.sshport, self.ip, self.username, self.ip)
        child = pexpect.spawn(cmd1)
        child.expect ('password:', timeout=None)
        child.sendline(self.passwd)

        child.interact()
        child.close()

        #----------------------------------------

def main():
    # data  from DB.
    # pass    

    #for eachlog in os.listdir('./remote_install/logs/'):
    #    os.remove('./remote_install/logs/%s' % eachlog)

    beanstalk = beanstalkc.Connection(
                                        host = '127.0.0.1',
                                        port = 11300,
                                        parse_yaml = lambda x: x.split('\n')
                                     )
    beanstalk.use('default')
    beanstalk.ignore('weblogic')
    beanstalk.use('weblogic')

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

    iplist.remove(master_ip)
    iplist.insert(0, master_ip)
    # -- for ---
    try:
        ff = open('/root/.ssh/known_hosts', 'w')
        ff.close()
    except IOError:
        pass

    for eachip in iplist:
        index = iplist.index(eachip)
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
    
        eachip = eachip.strip()
        D = distribute(eachip, hostusername, hostpassword, hostport)
        D.issued()
        
        if iplist[0] == eachip:
            tempdata = {'ip': eachip, 'role': 'admin'}
        else:
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
