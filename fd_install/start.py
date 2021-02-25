#!/usr/bin/env python

import os
import subprocess
from prase import prase_config

def handle():
#    subprocess.Popen('/usr/local/bin/beanstalkd &', shell=True)

    P = subprocess.Popen('python ./distribute.py',shell=True)
    os.system('python ./create_run.py')
    P.wait()

#    for line in os.listdir('/proc'):
#        try:
#            pid = int(line)
#        except ValueError:
#            continue
#        ff = open('/proc/%d/cmdline' % pid, 'r')
#        data = ff.readlines()
#        ff.close()
#        if 'beanstalkd' in str(data):
#            os.kill(pid, 9)
#            break

def loopback():
    count = 0
    pathdir = './remote_install/logs/'
    ff = open('/opt/autooption/flag.lock', 'r')
    tempdata = str(ff.readlines()[0]).strip()
    ff.close()
    iplist = prase_config('distribute', 'distip').strip().split(' ')
    while '' in iplist:
        iplist.remove('')
    for eachline in iplist:
        eachfile = eachline + '_log'
        ff = open(pathdir + eachfile, 'r')
        data  = str(ff.readlines())
        ff.close()
        if not 'trackerServer start successfully' in data:
            tempdata = tempdata[0] + tempdata[1] + tempdata[2] + tempdata[3] + '2'
            ff = open('/opt/autooption/flag.lock', 'w')
            ff.write(tempdata)
            ff.close()
            os._exit(0)
        elif not 'storageServer start successfully' in data:
            tempdata = tempdata[0] + tempdata[1] + tempdata[2] + tempdata[3] + '2'
            ff = open('/opt/autooption/flag.lock', 'w')
            ff.write(tempdata)
            ff.close()
            os._exit(0)

        else:
            count +=1
    
    if count == len(iplist):
        ff = open('/opt/autooption/flag.lock', 'r')
        data = str(ff.readlines()[0]).strip()
        ff.close()
        data = data[0] + data[1] + data[2] + data[3] + '1'
        ff = open('/opt/autooption/flag.lock', 'w')
        ff.write(data)
        ff.close()

if __name__ == '__main__':
    handle()
    loopback()
