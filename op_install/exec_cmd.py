#!/usr/bin/python 
# -*- coding:UTF-8 -*-

import paramiko

def ssh2(ip, port, username, passwd, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, int(port), username, passwd, timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            # stdin.write("Y")
            out = stdout.readlines()
            #print out
            #for o in out:
            #    print o,
            #    print '%s\tOK\n'%(ip)
            #    ssh.close()
        ssh.close()
        return out
    except Exception as e:
        pass


if __name__=='__main__':
    cmd = ['cat /etc/redhat-release']
    username = "root"
    passwd = "qwer1234"    
    ip = '172.17.78.89'
    port = '22'
    print ssh2(ip, port, username, passwd, cmd)
