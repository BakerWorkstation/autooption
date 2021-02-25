#!/usr/bin/env python

import os

os.chdir('software')
os.system('cd gcc-c++/ &&\
rpm -Uvh --replacepkgs *.rpm --force --nodeps &> /dev/null\
 && cd ..')


os.system('cd pexpect-4.2.1/ &&\
python setup.py install && cd ..')

os.system('cd ptyprocess-0.5.1/ &&\
python setup.py install && cd ..')

os.system('cd beanstalkc-0.4.0/ &&\
python setup.py install && cd ..')

os.system('cd django-1.6.11/ &&\
python setup.py install && cd ..')

os.chdir('beanstalkd')
os.chmod('beanstalkd', 777)
os.chmod('vers.sh', 777)
os.chmod('verc.sh', 777)
os.system('make clean && make && make install && cd ..')
os.chdir('..')
