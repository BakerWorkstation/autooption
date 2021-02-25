#!/usr/bin/env python

import os
import re
import sys
import ConfigParser

def handle():
    dblist = ['oracle', 'mysql', 'postgresql']  
 
    while 1:
        os.system('clear')
        print '''
        \n\n\n\t\t\t\t    \033[33mWelcome to configurate JDBC Centos%s.X\033[0m
        '''  % sys.argv[1]

        while 1:
            print '''\n\t\tFirst. Input the database type,for example( oracle, mysql, postgresql),choose one!
             \033[31minput >\033[0m''',
            dbtype = raw_input()
            if dbtype in dblist:
                break
            elif dbtype.strip() == '':
                dbtype = 'oracle'
                print '\t     dbtype : %s' % dbtype
                break
            else:
                print 'Warning : format mistake !'
      
        while 1:
            print '''\n\t\tSecond. Input the remote database`s ip address.
             \033[31minput >\033[0m''',
            ip = raw_input()
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip.strip()):
                break
            else:
                print 'Warning : format mistake!'
    
        while 1:
            print '''\n\t\tThird. Input the remote database`s port.
             \033[31minput >\033[0m''',
            port = raw_input()
            if re.match(r'^\d{4,5}$', port.strip()):
                break
            elif port.strip() == '':
                if dbtype.strip() == 'oracle':
                    port = '1521'
                    print '\t     port : %s' % port
                if dbtype.strip() == 'postgresql':
                    port = '5432'
                    print '\t     port : %s' % port
                if dbtype.strip() == 'mysql':
                    port = '3306'
                    print '\t     port : %s' % port
                break
            else:
                print 'Warning : format mistake!'
    
        while 1:
            print '''\n\t\tFourth. Input the database`s name or instance`s name.
             \033[31minput >\033[0m''',
            dbname = raw_input()
            if dbname.strip() == '':
                if dbtype.strip() == 'oracle':
                    dbname = 'orcl'
                    print '\t     instant : %s' % dbname
                    break
                else:
                    print 'Warning : format mistake!'
            else:
                break
  
        while 1:
            print '''\n\t\tFifth. Input the database`s username.
             \033[31minput >\033[0m''',
            user = raw_input()
            if user.strip() == '':
                print 'Warning : format mistake!'
            else:
                break
                
        while 1:
            print '''\n\t\tSixth. Input the database`s password
             \033[31minput >\033[0m''',
            passwd = raw_input()
            if passwd.strip() == '':
                print 'Warning : format mistake!'
            else:
                break
                
        while 1:
            os.system('clear')
            print '''Please ensure the message correctly:
        
                   \033[35m1.\033[0m  Database :  %s
                   \033[35m2.\033[0m  Ip       :  %s
                   \033[35m3.\033[0m  Port     :  %s
                   \033[35m4.\033[0m  Instant  :  %s
                   \033[35m5.\033[0m  Username :  %s
                   \033[35m6.\033[0m  Password :  %s
             
                If all rigth, please input 'Y' or 'y'.
                If have problem, please input the number to modify it.
                If you want to go back to configurate again, please input the other key.
                
        \033[31minput >\033[0m''' % ( dbtype, ip, port, dbname, user, passwd),
            choose = raw_input()

            if choose == '1':
                while 1:
                    print '''\n\033[5;36mConfigurate the database type again\033[0m
        \033[31minput >\033[0m''',
                    dbtype = raw_input()
                    if dbtype in dblist:
                    #if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', dbtype.strip()):
                        break
                    else:
                        print 'Warning : format mistake!'
            
            if choose == '2':
                while 1:
                    print '''\n\033[5;36mConfigurate the ip address again\033[0m
        \033[31minput >\033[0m''',
                    ip = raw_input()
                    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip.strip()):
                        break
                    else:
                        print 'Warning : format mistake!'

            if choose == '3':
                 while 1:
                    print '''\n\033[5;36mConfigurate the port again\033[0m
        \033[31minput >\033[0m''',
                    port = raw_input()
                    if re.match(r'^\d{4,5}$', port.strip()):
                        break
                    else:
                        print 'Warning : format mistake!'

            if choose == '4':
                print '''\n\033[5;36mConfigurate the instant again\033[0m
        \033[31minput >\033[0m''',
                dbname = raw_input()

            if choose == '5':
                print '''\n\033[5;36mConfigurate the username again\033[0m
        \033[31minput >\033[0m''',
                user = raw_input()

            if choose == '6':
                print '''\n\033[5;36mConfigurate the password again\033[0m
        \033[31minput >\033[0m''',
                passwd  = raw_input()

            if choose in 'Yy':
                break

            elif choose not in '123456yY':
                break

        scp = ConfigParser.ConfigParser()
        if choose in 'Yy':
            scp.add_section('database')
            scp.set('database', 'dbtype', dbtype.strip())
            scp.set('database', 'ip', ip.strip())
            scp.set('database', 'port', port.strip())
            scp.set('database', 'dbname', dbname.strip())
            scp.set('database', 'user', user.strip())
            scp.set('database', 'passwd', passwd.strip())
            os.system('clear')
            print '''\n\n\n\n\n\t\t    If want to join th cluster \
environment ?  ('y|Y' or 'n|N')\n\t\t\033[31minput >\033[0m''',
            choose = raw_input().strip()
            if choose in 'Yy':
                print '''\n\t\t    Please input the whole ip_address in \
the cluster,use space as the split\n\t\t    for example:  \
"input > ip1 ip2 ip3 ip4"\n\t\t\033[31minput >\033[0m''',
                iplist = raw_input().strip()
                scp.add_section('cluster')
                scp.set('cluster', 'enabled', '1')
                scp.set('cluster', 'iplist', iplist)
                scp.write(open('./define.cfg', 'w'))
            else:
                scp.add_section('cluster')
                scp.set('cluster', 'enabled', '0')
                scp.write(open('./define.cfg', 'w'))
                
            break
    print '''\n\t \033[32mConfig finish!\033[0m'''
    

if __name__ == '__main__':
    try:
        handle()
    except KeyboardInterrupt as e:
        print ''
        os._exit(0)
    except EOFError as e:
        print ''
        os._exit(0)
