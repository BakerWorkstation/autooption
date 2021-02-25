#!/usr/bin/env python

import os
import paramiko

def sftp_upload_dir(remote_dir, local_dir, ip, username, passwd, port):
    try:
        t = paramiko.Transport((ip, int(port)))
        t.connect(username=username, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        for root,dirs,files in os.walk(local_dir):
            for filespath in files:
                local_file = os.path.join(root,filespath)
                a = local_file.replace(local_dir,'')
                remote_file = os.path.join(remote_dir,a)
                try:
                    sftp.put(local_file,remote_file)
                except Exception,e:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file,remote_file)
            for name in dirs:
                local_path = os.path.join(root,name)
                a = local_path.replace(local_dir,'')
                remote_path = os.path.join(remote_dir,a)
                try:
                    sftp.mkdir(remote_path)
                except Exception,e:
                    print e
        t.close()
    except Exception,e:
        print e
#if __name__=='__main__':
#    remote_dir='/tmp/ban/'
#    local_dir='/mnt/ban/'
#    ip = '172.17.78.89'
#    username = 'root'
#    passwd = 'qwer1234'
#    port = '22'
#    sftp_upload_dir(remote_dir, local_dir, ip, username, passwd, port)
