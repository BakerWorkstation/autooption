# -*- coding:utf-8 -*-

import paramiko

def sftp_upload_file(server_path, local_path, ip, username, passwd, port):
    try:
        t = paramiko.Transport((ip, int(port)))
        t.connect(username=username, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
    except Exception, e:
        print e

#if __name__ == '__main__':
#    sftp_upload_file("/tmp/passwd", "/etc/passwd")
