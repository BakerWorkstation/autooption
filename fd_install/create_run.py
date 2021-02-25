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

    def compose(self):
         
        self.alldir = './remote_install/FastDFS_Install'
        runfile = '%s/FastDFS_Install.run' % self.alldir

        #if not os.path.exists(runfile):
        confdir = os.path.join(self.alldir, 'conf')
        conffile = os.path.join(confdir, 'fastdfs.cfg')
        if os.path.exists(conffile):
            os.remove(conffile)
        shutil.copyfile('./fastdfs.cfg', conffile)
         
        self.__L.info('#--- config start ---#')
        ff = open(conffile, 'r')
        for eachline in ff.readlines():
            if not eachline == '':
                self.__L.info(eachline.strip())
        self.__L.info('#--- config end ---#')

        tmp_tar_dir = './remote_install'
        file_name = "fastdfs_install.tar.gz"
        soft_name = "FastDFS_Install"
        tar = tarfile.open(os.path.join(tmp_tar_dir,file_name),"w:gz")  
        for root,dir,files in os.walk(os.path.join(tmp_tar_dir,soft_name)):  
            root_ = os.path.relpath(root,start=tmp_tar_dir)  
            for file in files:  
                full_path = os.path.join(root,file)  
                tar.add(full_path,arcname=os.path.join(root_,file))  
        tar.close()

        g = open('%s/FastDFS_Install.run' % tmp_tar_dir, 'w')
        f = open('%s/config.sh' % tmp_tar_dir, 'r')
        for eachline in  f.readlines():
            g.write(eachline)
        f.close()
        f = open('%s/fastdfs_install.tar.gz' % tmp_tar_dir, 'r')
        for eachline in  f.readlines():
            g.write(eachline)
        f.close()
        g.close()
        os.remove('%s/fastdfs_install.tar.gz' % tmp_tar_dir)
    

    def issued(self):
         
        sftp_upload_file('/tmp/FastDFS_Install.run',  # remote_filename
                         'remote_install/FastDFS_Install.run', # local_filename
                          self.ip,
                          self.username,
                          self.passwd,
                          self.port)
    

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
    beanstalk.ignore('fastdfs')
    beanstalk.use('fastdfs')


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
    

    # -- for ---
    #try:
    #    ff = open('/root/.ssh/known_hosts', 'w')
    #    ff.close()
    #except IOError:
    #    pass

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
        D.compose()
        D.issued()

        tempdata = {'ip': eachip}
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
