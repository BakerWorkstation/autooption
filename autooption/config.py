#!/usr/bin/env python
#! -*- coding:UTF-8 -*-


import os
import re
import commands
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


from pexpect import pxssh
import ConfigParser


def _get_path():
    path = sys.path[0]
    #print path
    path = '/opt/autooption/autooption'
    return path
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
    

def _check_ip(ip):
    """Returns true if the given string is a well-formed IP address."""
    addr = ip.strip().split('.')
    if len(addr) != 4:
        return False
    for i in range(4):
        try:
            addr[i]=int(addr[i])
        except:
            return False
        if addr[i]<=255 and addr[i]>=0:
            pass
        else:
            return False
        i+=1
    return True

def check_string(word):
    print word
    if re.match(r'^[a-zA-Z\_][0-9a-zA-Z\_]+', word):
        return True
    else:
        return False

############ weblogic #############
def wl_read():
    path = _get_path()
    config = ConfigParser.ConfigParser()
    config.read(path+'/weblogic.cfg')
    
    wl_nodenum = config.get('weblogic', 'wl_nodenum')
    wl_usertype = config.get('weblogic', 'wl_usertype')
    wl_domainname = config.get('weblogic', 'wl_domainname')
    wl_listenport = config.get('weblogic', 'wl_listenport')
    wl_clustername = config.get('weblogic', 'wl_clustername')
    wl_username = config.get('weblogic', 'wl_username')
    wl_password = config.get('weblogic', 'wl_password')
    wl_httpport = config.get('weblogic', 'wl_httpport')
    wl_memsize = config.get('weblogic', 'wl_memsize')
    wl_namelist = config.get('weblogic', 'wl_namelist')
    wl_iplist = config.get('weblogic', 'wl_iplist')
    wl_adminserver = config.get('weblogic', 'wl_adminserver')
    #host
    wl_hostusername = config.get('weblogic', 'wl_hostusername')
    wl_hostpassword = config.get('weblogic', 'wl_hostpassword')
    wl_hostsshport = config.get('weblogic', 'wl_hostsshport')
    
    dictdata = {'wl_nodenum': wl_nodenum,
              'wl_usertype': wl_usertype,
              'wl_domainname': wl_domainname,
              'wl_listenport': wl_listenport,
              'wl_clustername': wl_clustername,
              'wl_username': wl_username,
              'wl_password': wl_password,
              'wl_httpport': wl_httpport,
              'wl_memsize': wl_memsize,
              'wl_namelist': wl_namelist,
              'wl_iplist': wl_iplist,
              'wl_adminserver': wl_adminserver,
              'wl_hostusername': wl_hostusername,
              'wl_hostpassword': wl_hostpassword,
              'wl_hostsshport': wl_hostsshport}
    return dictdata


def wl_check(kwargs):
    wl_nodenum = kwargs['wl_nodenum']
    wl_usertype = kwargs['wl_usertype']
    wl_domainname = kwargs['wl_domainname']
    wl_listenport = kwargs['wl_listenport']
    wl_clustername = kwargs['wl_clustername']
    wl_username = kwargs['wl_username']
    wl_password = kwargs['wl_password']
    wl_httpport = kwargs['wl_httpport']
    wl_memsize = kwargs['wl_memsize']
    wl_namelist = kwargs['wl_namelist']
    wl_iplist = kwargs['wl_iplist']
    wl_adminserver = kwargs['wl_adminserver']
    wl_hostusername = kwargs['wl_hostusername']
    wl_hostpassword = kwargs['wl_hostpassword']
    wl_hostsshport = kwargs['wl_hostsshport']
    error_info = (u'')
    #check wl_nodenum, 1-4
    #check wl_usertype
    if wl_usertype != 'root' and wl_usertype != 'weblogic':
        error_info = error_info + (u'主机用户权限必须为root或weblogic！\n')
    #check wl_domainname
    if not wl_domainname.isalnum():
        error_info = error_info + (u'域名请使用字母或数字！\n')
    #check wl_listenport
    if not (wl_listenport.isdigit() and 6000 <= float(wl_listenport) <= 65535):
        error_info = error_info + (u'集群监听端口应为6000至65535！\n')
    #check wl_clustername
    if not wl_clustername.isalnum():
        error_info = error_info + (u'集群名称请使用字母或数字！\n')
    #check wl_username
    if not wl_username.isalnum():
        error_info = error_info + (u'web用户名请使用字母或数字！\n')
    #check wl_password
    if not (wl_password.isalnum() and not wl_password.isalpha() and not wl_password.isdigit()):
        error_info = error_info + (u'web登录密码必须使用字母和数字！\n')
    #check wl_httpport
    if not (wl_httpport.isdigit() and 6000 <= float(wl_httpport) <= 65535):
        error_info = error_info + (u'web监听端口应为6000至65535！\n')
    #check wl_memsize
    if not (wl_memsize.isdigit() and 1 <= float(wl_memsize) <= 99):
        error_info = error_info + (u'内存占用百分比1至99！\n')
    #check wl_namelist
    wl_namelist = wl_namelist.split(' ')
    if len(wl_namelist) != int(wl_nodenum):
        error_info = error_info + (u'请确认集群节点名称个数！\n')
    else:
        for info in wl_namelist:
            if not info:
                error_info = error_info + (u'集群节点名称不能为空！\n')
                break
    #check wl_iplist
    wl_iplist = wl_iplist.split(' ')
    if len(wl_iplist) != int(wl_nodenum):
        error_info = error_info + (u'请确认集群节点IP个数！\n')
    else:
        for info in wl_iplist:
            if not _check_ip(info):
                error_info = error_info + (u'集群节点IP格式错误！\n')
                break
    #check wl_adminserver
    #check wl_host
    wl_hostusername = wl_hostusername.split(' ')
    wl_hostpassword = wl_hostpassword.split(' ')
    wl_hostsshport = wl_hostsshport.split(' ')
    if not (len(wl_hostusername) == len(wl_hostpassword) == len(wl_hostsshport) == 1 or len(wl_hostusername) == len(wl_hostpassword) == len(wl_hostsshport) == int(wl_nodenum)):
        error_info = error_info + (u'请确认主机用户名、主机密码、主机端口个数！\n')
    else:
    #check wl_hostusername
        for info in wl_hostusername:
            if not info.isalnum():
                error_info = error_info + (u'主机用户名请使用字母或数字！\n')
                break
    #check wl_hostpassword
        for info in wl_hostpassword:
            if not info:
                error_info = error_info + (u'主机密码不能为空！\n')
                break
    #check wl_hostsshport
        for info in wl_hostsshport:
            if not (info.isdigit() and 0 <= float(info) <= 65535):
                error_info = error_info + (u'主机端口为0至65535的正整数！\n')
    
    return error_info


def wl_write(kwargs):
    path = _get_path()

    scp = ConfigParser.ConfigParser()
    
    wl_namelist = kwargs['wl_namelist'].split(' ')
    wl_iplist = kwargs['wl_iplist'].split(' ')
    wl_as_name = kwargs['wl_adminserver'].split(' ')[0]
    wl_as_ip = kwargs['wl_adminserver'].split(' ')[1]
    scp.add_section('weblogic')
    scp.set('weblogic', 'wl_nodenum', kwargs['wl_nodenum'])
    scp.set('weblogic', 'wl_usertype', kwargs['wl_usertype'])
    scp.set('weblogic', 'wl_domainname', kwargs['wl_domainname'])
    scp.set('weblogic', 'wl_listenport', kwargs['wl_listenport'])
    scp.set('weblogic', 'wl_clustername', kwargs['wl_clustername'])
    scp.set('weblogic', 'wl_username', kwargs['wl_username'])
    scp.set('weblogic', 'wl_password', kwargs['wl_password'])
    scp.set('weblogic', 'wl_httpport', kwargs['wl_httpport'])
    scp.set('weblogic', 'wl_memsize', kwargs['wl_memsize'])
    scp.set('weblogic', 'wl_namelist', kwargs['wl_namelist'])
    scp.set('weblogic', 'wl_iplist', kwargs['wl_iplist'])
    scp.set('weblogic', 'wl_adminserver', kwargs['wl_adminserver'])
    scp.set('weblogic', 'wl_hostusername', kwargs['wl_hostusername'])
    scp.set('weblogic', 'wl_hostpassword', kwargs['wl_hostpassword'])
    scp.set('weblogic', 'wl_hostsshport', kwargs['wl_hostsshport'])
    scp.write(open(path+'/weblogic.cfg', 'w'))
    
    cmd = 'rm -rf ' + path + '/wl_*.cfg'
    commands.getstatusoutput(cmd)

    templist = []
    wl_hostusernamelist = kwargs['wl_hostusername'].split(' ')
    wl_hostpasswordlist = kwargs['wl_hostpassword'].split(' ')
    wl_hostsshportlist = kwargs['wl_hostsshport'].split(' ')
    print wl_iplist
    for num, eachip in enumerate(wl_iplist):
        cmd = "ifconfig | grep 'inet addr' | grep -v '127.0.0.1' | awk -F ':' '{print $2}' | awk '{print $1}' |sed -n 1p"
        #res = commands.getstatusoutput(cmd)
        # username
        try:
            hostusername = wl_hostusernamelist[num]
        except:
            hostusername = wl_hostusernamelist[0]
        # password
        try:
            hostpassword = wl_hostpasswordlist[num]
        except:
            hostpassword = wl_hostpasswordlist[0]
        # port
        try:
            hostport = wl_hostsshportlist[num]
        except:
            hostport = wl_hostsshportlist[0]
        # connect
        try:
            s = pxssh.pxssh()
            s.login(str(eachip), hostusername, hostpassword, port=hostport)
            #error_info += (u'%s, ssh连接成功！\n' % eachip)
            print 'login success'
            s.sendline(cmd)
            s.prompt()
            hostip = s.before.split('\n')[-2].replace('\r', '')
            print hostip
            s.close()
            templist.append(hostip)
            print cmd
            #hostip = res[1]
            if eachip == wl_as_ip:
                wl_as_ip = hostip
        except Exception, e:
            print str(e)
            #error_info += (u'%s, ssh连接失败！\n' % eachip)
            return False

    wl_local_iplist = ' '.join(templist)
    
    for num, ip in enumerate(wl_iplist):
        scp.remove_section('weblogic')
        scp.add_section('weblogic')
        scp.set('weblogic', 'node_num', kwargs['wl_nodenum'])
        scp.set('weblogic', 'user_type', kwargs['wl_usertype'])
        scp.set('weblogic', 'domain_name', kwargs['wl_domainname'])
        scp.set('weblogic', 'listen_port', kwargs['wl_listenport'])
        scp.set('weblogic', 'cluster_name', kwargs['wl_clustername'])
        scp.set('weblogic', 'username', kwargs['wl_username'])
        scp.set('weblogic', 'password', kwargs['wl_password'])
        scp.set('weblogic', 'http_port', kwargs['wl_httpport'])
        scp.set('weblogic', 'mem_size', kwargs['wl_memsize'])
        scp.set('weblogic', 'server_name1', wl_as_name)
        scp.set('weblogic', 'listen_ip1', wl_as_ip)
        scp.set('weblogic', 'server_namelist', kwargs['wl_namelist'])
        #scp.set('weblogic', 'listen_iplist', kwargs['wl_iplist'])
        scp.set('weblogic', 'listen_iplist', wl_local_iplist)
        #if ip == wl_as_ip:
        if templist[num] == wl_as_ip:
            scp.set('weblogic', 'server_name2', '*')
            scp.set('weblogic', 'listen_ip2', '*')
        else:
            scp.set('weblogic', 'server_name2', wl_namelist[num])
            #scp.set('weblogic', 'listen_ip2', wl_iplist[num])
            scp.set('weblogic', 'listen_ip2', templist[num])
        scp.write(open(path+'/wl_'+ip+'.cfg', 'w'))
    return True


############ openfire #############
def op_read():
    path = _get_path()
    
    config = ConfigParser.ConfigParser()
    config.read(path+'/openfire.cfg')
    
    op_dbtype = config.get('database', 'dbtype')
    op_dbip = config.get('database', 'ip')
    op_dbport = config.get('database', 'port')
    op_instant = config.get('database', 'dbname')
    op_dbusername = config.get('database', 'user')
    op_dbpasswd = config.get('database', 'passwd')
    op_memsize = config.get('database', 'memsize')
    op_webport = config.get('database', 'webport')

    switch = config.get('cluster', 'enabled')
    if switch == '1':
        op_clusterip = config.get('cluster', 'iplist')
    else:
        op_clusterip = ''
    
    op_distip = config.get('distribute', 'distip')
    op_username = config.get('distribute', 'username')
    op_password = config.get('distribute', 'password')
    op_hostport = config.get('distribute', 'hostport')
    dictdata = {'op_dbtype': op_dbtype,
                'op_dbip': op_dbip,
                'op_dbport': op_dbport,
                'op_instant': op_instant,
                'op_dbusername': op_dbusername,
                'op_dbpasswd': op_dbpasswd,
                'op_memsize': op_memsize,
                'op_webport': op_webport,
                'op_clusterip': op_clusterip,
                'op_hostip': op_distip,
                'op_hostusername': op_username,
                'op_hostpassword': op_password,
                'op_hostport': op_hostport}
    return dictdata



def op_check(kwargs):
    dbtype = kwargs['op_dbtype'].encode('utf-8')
    dbip = kwargs['op_dbip'].encode('utf-8')
    dbport = kwargs['op_dbport'].encode('utf-8')
    instant = kwargs['op_instant'].encode('utf-8')
    dbusername = kwargs['op_dbusername'].encode('utf-8')
    dbpasswd = kwargs['op_dbpasswd'].encode('utf-8')
    memsize = kwargs['op_memsize'].encode('utf-8')
    webport = kwargs['op_webport'].encode('utf-8')
    clusterip = kwargs['op_clusterip'].encode('utf-8')
    hostip = kwargs['op_hostip'].encode('utf-8')
    hostusername = kwargs['op_hostusername'].encode('utf-8')
    hostpassword = kwargs['op_hostpassword'].encode('utf-8')
    hostport = kwargs['op_hostport'].encode('utf-8')
    
    error_info = (u'')
    # check dbtype
    dblist = ['oracle', 'mysql', 'postgresql']
    if not dbtype.strip() in dblist:
        error_info += (u'数据库类型为oracle、mysql、postgresql之一！\n')
    # check dbip
    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', dbip.strip()):
        error_info += (u'数据库IP格式错误！\n')
    # check dbport
    if not re.match(r'^\d{4,5}$', dbport.strip()):
        error_info += (u'数据库端口错误！\n')
    # check instant
    flag = check_string(instant.strip())
    if not flag:
        error_info += (u'数据库实例名不是合法字符串！\n')
    # check dbusername
    flag = check_string(dbusername.strip())
    if not flag:
        error_info += (u'数据库用户名不是合法字符串！\n')
    # check dbpasswd
    flag = check_string(dbpasswd.strip())
    if not flag:
        error_info += (u'数据库密码不是合法字符串！\n')
    # check memsize
    if not re.match(r'^\d{2}$', memsize.strip()):
        error_info += (u'Java启动内存参数错误！\n')
    # check webport
    try:
        tmpport = int(webport.strip())
        if not (tmpport >= 6000 and tmpport <= 65535):
            error_info += (u'web访问端口错误！\n')
    except Exception:
        error_info += (u'web访问端口错误！\n')
    # check clusterip
    for eachip in clusterip.strip().split(' '):
        if eachip == '':
            continue
        else:
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', eachip):
                error_info += (u'集群IP格式错误！\n')

    iplist = hostip.strip().split(' ')
    while '' in iplist:
        iplist.remove('')

    usernamelist = hostusername.strip().split(' ')
    while '' in usernamelist:
        usernamelist.remove('')

    passwordlist = hostpassword.strip().split(' ')
    while '' in passwordlist:
        passwordlist.remove('')

    portlist = hostport.strip().split(' ')
    while '' in portlist:
        portlist.remove('')
    len_ip = len(iplist)
    len_user = len(usernamelist)
    len_pd = len(passwordlist)
    len_port = len(portlist)
    if not (len_user == len_ip or len_user == 1):
        return '主机用户名数量有误'

    if not (len_pd == len_ip or len_pd == 1):
        return '主机密码数量有误'

    if not (len_port == len_ip or len_port == 1):
        return '主机端口数量有误'

    # check hostip
    for eachline in iplist:
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', eachline):
            error_info += (u'下发主机IP格式错误！\n')
            break
    # check hostusername
    for eachline in usernamelist:
        flag = check_string(eachline)
        if not flag:
            error_info += (u'下发主机用户名不是合法字符串！\n')
            break
    # check hostpassword
    for eachline in passwordlist:
        flag = check_string(eachline)
        if not flag:
            error_info += (u'下发主机密码不是合法字符串！\n')
            break
    # check hostport
    for eachline in portlist:
        if not re.match(r'^\d{2,5}$', eachline):
            error_info += (u'主机端口格式错误！\n')
            break
    return error_info


def op_write(kwargs):
    path = _get_path()

    scp = ConfigParser.ConfigParser()

    scp.add_section('database')
    scp.set('database', 'dbtype', kwargs['op_dbtype'])
    scp.set('database', 'ip', kwargs['op_dbip'])
    scp.set('database', 'port', kwargs['op_dbport'])
    scp.set('database', 'dbname', kwargs['op_instant'])
    scp.set('database', 'user', kwargs['op_dbusername'])
    scp.set('database', 'passwd', kwargs['op_dbpasswd'])
    scp.set('database', 'memsize', kwargs['op_memsize'])
    scp.set('database', 'webport', kwargs['op_webport'])

    scp.add_section('cluster')
    if kwargs['op_clusterip'].strip():
        scp.set('cluster', 'enabled', '1')
        scp.set('cluster', 'iplist', kwargs['op_clusterip'])
    else:
        scp.set('cluster', 'enabled', '0')

    scp.add_section('distribute')
    scp.set('distribute', 'distip', kwargs['op_hostip'])
    scp.set('distribute', 'username', kwargs['op_hostusername'])
    scp.set('distribute', 'password', kwargs['op_hostpassword'])
    scp.set('distribute', 'hostport', kwargs['op_hostport'])

    scp.write(open(path+'/openfire.cfg', 'w'))

    
    
    
############ oracle #############
def or_read():
    path = _get_path()
    config = ConfigParser.ConfigParser()
    config.read(path+'/oracle.cfg')
    
    or_port = config.get('oracle', 'or_port')
    or_instancename = config.get('oracle', 'or_instancename')
    or_charset = config.get('oracle', 'or_charset')
    or_logsize = config.get('oracle', 'or_logsize')
    or_memsize = config.get('oracle', 'or_memsize')
    or_process = config.get('oracle', 'or_process')
    #host
    or_hostusername = config.get('oracle', 'or_hostusername')
    or_hostpassword = config.get('oracle', 'or_hostpassword')
    or_hostip = config.get('oracle', 'or_hostip')
    or_hostsshport = config.get('oracle', 'or_hostsshport')
    
    dictdata = {'or_port': or_port,
              'or_instancename': or_instancename,
              'or_charset': or_charset,
              'or_logsize': or_logsize,
              'or_memsize': or_memsize,
              'or_process': or_process,
              'or_hostusername': or_hostusername,
              'or_hostpassword': or_hostpassword,
              'or_hostip': or_hostip,
              'or_hostsshport': or_hostsshport}
    return dictdata


def or_check(kwargs):
    or_port = kwargs['or_port']
    or_instancename = kwargs['or_instancename']
    or_charset = kwargs['or_charset']
    or_logsize = kwargs['or_logsize']
    or_memsize = kwargs['or_memsize']
    or_process = kwargs['or_process']
    #host
    or_hostusername = kwargs['or_hostusername']
    or_hostpassword = kwargs['or_hostpassword']
    or_hostip = kwargs['or_hostip']
    or_hostsshport = kwargs['or_hostsshport']
    print kwargs
    error_info = (u'')
    #check or_port
    if not (or_port.isdigit() and 1000 <= float(or_port) <= 65535):
        error_info = error_info + (u'oracle端口号范围1000~65535！\n')
    #check or_instancename
    if not ( 3 <= len(or_instancename) <= 20 ):
        error_info = error_info + (u'实例名长度范围3~20！\n')
    elif not or_instancename.isalnum():
        error_info = error_info + (u'实例名请使用字母或数字！\n')
    elif not or_instancename[0].isalpha():
        error_info = error_info + (u'实例名首位必须为字母！\n')
    #check or_charset
    #check or_logsize
    if not or_logsize.isdigit():
        error_info = error_info + (u'日志大小请输入正整数！\n')
    #check or_memsize
    if not (or_memsize.isdigit() and 40 <= float(or_memsize) <= 80):
        error_info = error_info + (u'内存占用百分比40至80！\n')
    #check or_process
    if not (or_process.isdigit() and 150 <= float(or_process) <= 2000):
        error_info = error_info + (u'进程数范围150至2000！\n')
    
    #check or_hostusername
    if not or_hostusername.isalnum():
        error_info = error_info + (u'主机用户名请使用字母或数字！\n')
    #check or_hostpassword
    if not or_hostpassword.isalnum():
        error_info = error_info + (u'主机密码请使用字母或数字！\n')
    #check or_hostpassword
    if not (or_hostsshport.isdigit() and 0 <= float(or_hostsshport) <= 65535):
        error_info = error_info + (u'主机端口范围0至65535！\n')
    #check or_hostip
    for eachip in or_hostip.strip().split(' '):
        if eachip == '':
            continue
        else:
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', eachip):
                error_info += (u'主机IP格式错误！\n')
    return error_info


def or_write(kwargs):
    path = _get_path()

    scp = ConfigParser.ConfigParser()
    
    scp.add_section('oracle')
    scp.set('oracle', 'or_port', kwargs['or_port'])
    scp.set('oracle', 'or_instancename', kwargs['or_instancename'])
    scp.set('oracle', 'or_charset', kwargs['or_charset'])
    scp.set('oracle', 'or_logsize', kwargs['or_logsize'])
    scp.set('oracle', 'or_memsize', kwargs['or_memsize'])
    scp.set('oracle', 'or_process', kwargs['or_process'])
    #host
    scp.set('oracle', 'or_hostusername', kwargs['or_hostusername'])
    scp.set('oracle', 'or_hostpassword', kwargs['or_hostpassword'])
    scp.set('oracle', 'or_hostip', kwargs['or_hostip'])
    scp.set('oracle', 'or_hostsshport', kwargs['or_hostsshport'])
    scp.write(open(path+'/oracle.cfg', 'w'))


############ mysql #############
def my_read():
    path = _get_path()
    config = ConfigParser.ConfigParser()
    config.read(path+'/mysql.cfg')
    
    #host
    my_hostusername = config.get('mysql', 'my_hostusername')
    my_hostpassword = config.get('mysql', 'my_hostpassword')
    my_hostip = config.get('mysql', 'my_hostip')
    my_hostsshport = config.get('mysql', 'my_hostsshport')
    
    dictdata = {'my_hostusername': my_hostusername,
              'my_hostpassword': my_hostpassword,
              'my_hostip': my_hostip,
              'my_hostsshport': my_hostsshport}
    return dictdata


def my_check(kwargs):
    #host
    my_hostusername = kwargs['my_hostusername']
    my_hostpassword = kwargs['my_hostpassword']
    my_hostip = kwargs['my_hostip']
    my_hostsshport = kwargs['my_hostsshport']
    print kwargs
    error_info = (u'')
    #check my_hostusername
    if not my_hostusername.isalnum():
        error_info = error_info + (u'主机用户名请使用字母或数字！\n')
    #check my_hostpassword
    if not my_hostpassword.isalnum():
        error_info = error_info + (u'主机密码请使用字母或数字！\n')
    #check my_hostpassword
    if not (my_hostsshport.isdigit() and 0 <= float(my_hostsshport) <= 65535):
        error_info = error_info + (u'主机端口范围0至65535！\n')
    #check or_hostip
    for eachip in my_hostip.strip().split(' '):
        if eachip == '':
            continue
        else:
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', eachip):
                error_info += (u'主机IP格式错误！\n')
    return error_info


def my_write(kwargs):
    path = _get_path()

    scp = ConfigParser.ConfigParser()
    
    scp.add_section('mysql')
    #host
    scp.set('mysql', 'my_hostusername', kwargs['my_hostusername'])
    scp.set('mysql', 'my_hostpassword', kwargs['my_hostpassword'])
    scp.set('mysql', 'my_hostip', kwargs['my_hostip'])
    scp.set('mysql', 'my_hostsshport', kwargs['my_hostsshport'])
    scp.write(open(path+'/mysql.cfg', 'w'))


def fd_read():
    path = _get_path()
    config = ConfigParser.ConfigParser()
    config.read(path+'/fastdfs.cfg')
    
    #host
    fd_hostusername = config.get('distribute', 'username')
    fd_hostpassword = config.get('distribute', 'password')
    fd_hostip = config.get('distribute', 'distip')
    fd_hostport = config.get('distribute', 'hostport')
    fd_trackerport = config.get('fastdfs', 'tracker_port')
    fd_storageport = config.get('fastdfs', 'storage_port')
    
    dictdata = {'fd_hostusername': fd_hostusername,
              'fd_hostpassword': fd_hostpassword,
              'fd_hostip': fd_hostip,
              'fd_hostport': fd_hostport,
              'fd_trackerport': fd_trackerport,
              'fd_storageport': fd_storageport}
    return dictdata

def fd_check(kwargs):
    #host
    fd_hostip = kwargs['fd_hostip'].encode('utf-8')
    fd_hostusername = kwargs['fd_hostusername'].encode('utf-8')
    fd_hostpassword = kwargs['fd_hostpassword'].encode('utf-8')
    fd_hostport = kwargs['fd_hostport'].encode('utf-8')
    fd_trackerport = kwargs['fd_trackerport'].encode('utf-8')
    fd_storageport = kwargs['fd_storageport'].encode('utf-8')
    #print kwargs
    error_info = (u'')
    # check trackerport
    try:
        tmpport = int(fd_trackerport.strip())
        if not (tmpport >= 0 and tmpport <= 65535):
            error_info += (u'trackerServer端口错误！\n')
    except Exception:
        error_info += (u'trackerServer端口错误！\n')
    # check storageport
    try:
        tmpport = int(fd_storageport.strip())
        if not (tmpport >= 0 and tmpport <= 65535):
            error_info += (u'storageServer端口错误！\n')
    except Exception:
        error_info += (u'storageServer端口错误！\n')

    iplist = fd_hostip.strip().split(' ')
    while '' in iplist:
        iplist.remove('')

    usernamelist = fd_hostusername.strip().split(' ')
    while '' in usernamelist:
        usernamelist.remove('')

    passwordlist = fd_hostpassword.strip().split(' ')
    while '' in passwordlist:
        passwordlist.remove('')

    portlist = fd_hostport.strip().split(' ')
    while '' in portlist:
        portlist.remove('')
    len_ip = len(iplist)
    len_user = len(usernamelist)
    len_pd = len(passwordlist)
    len_port = len(portlist)
    if not (len_user == len_ip or len_user == 1):
        return '主机用户名数量有误'

    if not (len_pd == len_ip or len_pd == 1):
        return '主机密码数量有误'

    if not (len_port == len_ip or len_port == 1):
        return '主机端口数量有误'

    # check hostip
    for eachline in iplist:
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', eachline):
            error_info += (u'下发主机IP格式错误！\n')
            break
    # check hostusername
    for eachline in usernamelist:
        flag = check_string(eachline)
        if not flag:
            error_info += (u'下发主机用户名不是合法字符串！\n')
            break
    # check hostpassword
    for eachline in passwordlist:
        flag = check_string(eachline)
        if not flag:
            error_info += (u'下发主机密码不是合法字符串！\n')
            break
    # check hostport
    for eachline in portlist:
        if not re.match(r'^\d{2,5}$', eachline):
            error_info += (u'主机端口格式错误！\n')
            break

    return error_info

def fd_write(kwargs):
    path = _get_path()

    scp = ConfigParser.ConfigParser()
    # config 
    scp.add_section('fastdfs')
    scp.set('fastdfs', 'tracker_port', kwargs['fd_trackerport'])
    scp.set('fastdfs', 'storage_port', kwargs['fd_storageport'])
    # host
    scp.add_section('distribute')
    scp.set('distribute', 'username', kwargs['fd_hostusername'])
    scp.set('distribute', 'password', kwargs['fd_hostpassword'])
    scp.set('distribute', 'distip', kwargs['fd_hostip'])
    scp.set('distribute', 'hostport', kwargs['fd_hostport'])

    scp.write(open(path+'/fastdfs.cfg', 'w'))
