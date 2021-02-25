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
from exec_cmd import ssh2
from upload_file import sftp_upload_file


class distribute(object):

    def __init__(self, ip, user, passwd, port):
        
        self.ip = ip
        self.username = user
        self.passwd = passwd
        self.port = port
        path = 'remote_install/logs/%s_log' % self.ip
        if os.path.exists(path):
            os.remove('./remote_install/logs/%s_log' % self.ip)
        self.__L = Logrecord(self.ip)
 
        # catch system version : Centos5 or Centos6

    def catch_version(self):
        flag = 1
        while 1:
            try:
                cmd = ['cat /etc/redhat-release']
                version = ssh2(self.ip, self.port, self.username, self.passwd, cmd)[0].replace('\n' ,'')
                self.__L.info(version)
                break
            except Exception:
                time.sleep(3)
                flag += 1
                if flag > 3:
                    version = ''
                    self.__L.error('network error(cat /etc/redhat-release)')
                    break

        if '5.' in version:
            # Centos5.x
            return 5

        elif '6.' in version:
           # Centos6.x
            return 6

    def compose(self, version):
         
        self.alldir = './remote_install/centos%s' % version
        runfile = '%s/openfire_install_centos%s.X.run' % (self.alldir, version)

        #if not os.path.exists(runfile):
        confdir = os.path.join(self.alldir, 'openfire_setup/conf')
        conffile = os.path.join(confdir, 'define.cfg')
        if os.path.exists(conffile):
            os.remove(conffile)
        #os.system('python patch_config.py %s' % version)
        shutil.copyfile('./openfire.cfg', conffile)
         
        self.__L.info('#--- config start ---#')
        ff = open('%s/define.cfg' % confdir, 'r')
        for eachline in ff.readlines():
            if not eachline == '':
                self.__L.info(eachline.strip())
        self.__L.info('#--- config end ---#')

        tmp_tar_dir = self.alldir
        file_name = "openfire_install.tar.gz"
        tar_dir = self.alldir
        soft_name = "openfire_setup"
        tar = tarfile.open(os.path.join(tmp_tar_dir,file_name),"w:gz")  
        for root,dir,files in os.walk(os.path.join(tar_dir,soft_name)):  
            root_ = os.path.relpath(root,start=tar_dir)  
            for file in files:  
                full_path = os.path.join(root,file)  
                tar.add(full_path,arcname=os.path.join(root_,file))  
        tar.close()

        g = open('%s/openfire_install_centos%s.X.run' % (self.alldir, version), 'w')
        f = open('%s/config.sh' % self.alldir, 'r')
        for eachline in  f.readlines():
            g.write(eachline)
        f.close()
        f = open('%s/openfire_install.tar.gz' % self.alldir, 'r')
        for eachline in  f.readlines():
            g.write(eachline)
        f.close()
        g.close()
        os.remove('%s/openfire_install.tar.gz' % self.alldir)
    

    def issued(self, version):
        sftp_upload_file('/tmp/openfire_install_centos%s.X.run' % version, 
                         '%s/openfire_install_centos%s.X.run' % (self.alldir, version), 
                         self.ip, 
                         self.username, 
                         self.passwd, 
                         self.port)

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
    beanstalk.ignore('openfire')
    beanstalk.use('openfire')


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
        data = D.catch_version()
        D.compose(data)
        D.issued(data)

        tempdata = {'version': data, 'ip': eachip}
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
