#!/user/bin/python
# -*- encoding: UTF-8 -*-
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.models import User, Permission, Group
from django.contrib import auth
from django import forms
from django.http import HttpResponseRedirect
import json
import httplib
import os
import os.path
import base64
import sys
import functools
import time
import datetime
import commands
import shutil
import subprocess

import config
import sethost
from pexpect import pxssh
from zabbix_api import get_data
from actual import ActuData
from history import HistData
from Mysql import connect
from patchReport import Create
from getHtml import patchHtml

import ConfigParser
from encrypt import encryuser

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)



def _get_path():
    path = sys.path[0]
    #print path
    path = '/opt/autooption/autooption'
    return path
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def _login_required(func):
    @functools.wraps(func)
    def wrap(request):
        try:
            if not request.user.is_authenticated() or not request.user.is_active:
                return render_to_response('login.html', context_instance = RequestContext(request))
        except Exception, e:
            return render_to_response('login.html', {'error_info':(u'数据库服务异常关闭！')}, context_instance = RequestContext(request))
        return func(request)
    return wrap




def default(request):
    return render_to_response('login.html', context_instance = RequestContext(request))


def login(request):
    ####
    #try:
    #    u = User.objects.create_user(username = 'admin', password = 'qwer1234')
    #except Exception, e:
    #    print e
    ####
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception, e:
        print e
        return render_to_response('login.html',{'error_info': (u'输入非法参数！')}, context_instance = RequestContext(request))
    try:
        user = auth.authenticate(username = username, password = password)
    except Exception, e:
        return render_to_response('login.html', {'error_info':(u'数据库服务异常关闭！')}, context_instance = RequestContext(request))
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            wl_data = config.wl_read()
            op_data = config.op_read()
            or_data = config.or_read()
            my_data = config.my_read()
            fd_data = config.fd_read()
            data = wl_data.copy()
            data.update(op_data)
            data.update(or_data)
            data.update(my_data)
            data.update(fd_data)
            #return render_to_response('menu.html',data, context_instance = RequestContext(request))
            return HttpResponseRedirect('/menu?show=ServiceDesk')
        else:
            return render_to_response('login.html', {'error_info':(u'该用户已被禁用！')}, context_instance = RequestContext(request))
    else:
        return render_to_response('login.html',{'error_info': (u'请确认用户名和密码！')}, context_instance = RequestContext(request))


def logout_user(request):
    try:
        auth.logout(request)
    except Exception, e:
        print e
    return render_to_response('login.html', context_instance = RequestContext(request))


@_login_required
def conf(request):
    wl_data = config.wl_read()
    op_data = config.op_read()
    or_data = config.or_read()
    my_data = config.my_read()
    fd_data = config.fd_read()
    data = wl_data.copy()
    data.update(op_data)
    data.update(or_data)
    data.update(my_data)
    data.update(fd_data)
    data['error_info'] = ''
    return render_to_response('config.html', data, context_instance = RequestContext(request))


def wl_setconf(request):
    error_info = (u'配置weblogic参数失败！')
    try:
        wl_nodenum = request.GET['wl_nodenum']
        wl_usertype = request.GET['wl_usertype']
        wl_domainname = request.GET['wl_domainname']
        wl_listenport = request.GET['wl_listenport']
        wl_clustername = request.GET['wl_clustername']
        wl_username = request.GET['wl_username']
        wl_password = request.GET['wl_password']
        wl_httpport = request.GET['wl_httpport']
        wl_memsize = request.GET['wl_memsize']
        wl_namelist = request.GET['wl_namelist']
        wl_iplist = request.GET['wl_iplist']
        wl_adminserver = request.GET['wl_adminserver']
        wl_hostusername = request.GET['wl_hostusername']
        wl_hostpassword = request.GET['wl_hostpassword']
        wl_hostsshport = request.GET['wl_hostsshport']
    except Exception, e:
        print str(e)
        return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')
    kwargs = {'wl_nodenum': wl_nodenum,
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
    error_info = config.wl_check(kwargs)
    if len(error_info) == 0:
        if config.wl_write(kwargs):
            error_info = (u'配置weblogic参数成功！')
        else:
            error_info = (u'配置weblogic参数失败！')
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')


def op_setconf(request):
    error_info = (u'配置openfire参数失败！')
    try:
        op_dbtype = request.GET['op_dbtype']
        op_dbip = request.GET['op_dbip']
        op_dbport = request.GET['op_dbport']
        op_instant = request.GET['op_instant']
        op_dbusername = request.GET['op_dbusername']
        op_dbpasswd = request.GET['op_dbpasswd']
        op_memsize = request.GET['op_memsize']
        op_webport = request.GET['op_webport']
        op_clusterip = request.GET['op_clusterip']
        op_hostip = request.GET['op_hostip']
        op_hostusername = request.GET['op_hostusername']
        op_hostpassword = request.GET['op_hostpassword']
        op_hostport = request.GET['op_hostport']
    except Exception, e:
        print str(e)
        return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')
    kwargs = {'op_dbtype': op_dbtype,
              'op_dbip': op_dbip,
              'op_dbport': op_dbport,
              'op_instant': op_instant,
              'op_dbusername': op_dbusername,
              'op_dbpasswd': op_dbpasswd,
              'op_memsize': op_memsize,
              'op_webport': op_webport,
              'op_clusterip': op_clusterip,
              'op_hostip': op_hostip,
              'op_hostusername': op_hostusername,
              'op_hostpassword': op_hostpassword,
              'op_hostport': op_hostport}
    error_info = config.op_check(kwargs)
    if len(error_info) == 0:
        config.op_write(kwargs)
        error_info = (u'配置openfire参数成功！')
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')


def or_setconf(request):
    error_info = (u'配置oracle参数失败！')
    try:
        or_port = request.GET['or_port']
        or_instancename = request.GET['or_instancename']
        or_charset = request.GET['or_charset']
        or_logsize = request.GET['or_logsize']
        or_memsize = request.GET['or_memsize']
        or_process = request.GET['or_process']
        or_hostusername = request.GET['or_hostusername']
        or_hostpassword = request.GET['or_hostpassword']
        or_hostip = request.GET['or_hostip']
        or_hostsshport = request.GET['or_hostsshport']
    except Exception, e:
        print str(e)
        return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')
    kwargs = {'or_port': or_port,
              'or_instancename': or_instancename,
              'or_charset': or_charset,
              'or_logsize': or_logsize,
              'or_memsize': or_memsize,
              'or_process': or_process,
              'or_hostusername': or_hostusername,
              'or_hostpassword': or_hostpassword,
              'or_hostip': or_hostip,
              'or_hostsshport': or_hostsshport}
    error_info = config.or_check(kwargs)
    if len(error_info) == 0:
        config.or_write(kwargs)
        error_info = (u'配置oracle参数成功！')
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')


def my_setconf(request):
    error_info = (u'配置mysql参数失败！')
    try:
        my_hostusername = request.GET['my_hostusername']
        my_hostpassword = request.GET['my_hostpassword']
        my_hostip = request.GET['my_hostip']
        my_hostsshport = request.GET['my_hostsshport']
    except Exception, e:
        print str(e)
        return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')
    kwargs = {'my_hostusername': my_hostusername,
              'my_hostpassword': my_hostpassword,
              'my_hostip': my_hostip,
              'my_hostsshport': my_hostsshport}
    error_info = config.my_check(kwargs)
    if len(error_info) == 0:
        config.my_write(kwargs)
        error_info = (u'配置mysql参数成功！')
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')


def fd_setconf(request):
    error_info = (u'配置fastdfs参数失败！')
    try:
        fd_hostusername = request.GET['fd_hostusername']
        fd_hostpassword = request.GET['fd_hostpassword']
        fd_hostip = request.GET['fd_hostip']
        fd_hostport = request.GET['fd_hostport']
        fd_trackerport = request.GET['fd_trackerport']
        fd_storageport = request.GET['fd_storageport']
        print fd_hostusername
    except Exception, e:
        print str(e)
        return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')
    kwargs = {'fd_hostusername': fd_hostusername,
              'fd_hostpassword': fd_hostpassword,
              'fd_hostip': fd_hostip,
              'fd_hostport': fd_hostport,
              'fd_trackerport': fd_trackerport,
              'fd_storageport': fd_storageport}
    error_info = config.fd_check(kwargs)
    if len(error_info) == 0:
        config.fd_write(kwargs)
        error_info = (u'配置fastdfs参数成功！')
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')


@_login_required
def install(request):
    install_info = {}
    install_info['wl_datetime'] = '-'
    install_info['wl_status'] = (u'未配置')
    install_info['op_datetime'] = '-'
    install_info['op_status'] = (u'未配置')
    install_info['or_datetime'] = '-'
    install_info['or_status'] = (u'未配置')
    install_info['my_datetime'] = '-'
    install_info['my_status'] = (u'未配置')
    install_info['fd_datetime'] = '-'
    install_info['fd_status'] = (u'未配置')
    

    wl_data = config.wl_read()
    op_data = config.op_read()
    or_data = config.or_read()
    my_data = config.my_read()
    fd_data = config.fd_read()


    op_iplist = op_data['op_hostip'].strip().split(' ')
    while '' in op_iplist:
        op_iplist.remove('')

    install_info['wl_adminserverip'] = (r'%s' % wl_data['wl_adminserver'].split(' ')[-1])
    install_info['wl_httpport'] = (r'%s' % wl_data['wl_httpport'])
    
    install_info['op_first'] = (r'%s' % op_iplist[0])
    try:
        install_info['op_two'] = (r'%s' % op_iplist[1])
    except:
        install_info['op_two'] = "false"
    
    op_webport = op_data['op_webport'].strip()
    install_info['op_webport'] = (r'%s' % op_webport)
   
    path = config._get_path()
    cmd = 'ls -alhG --full-time ' + path + '/weblogic.cfg'
    if wl_data['wl_hostpassword'] != '':
        res = commands.getstatusoutput(cmd)
        info_temp = res[1].split(' +0800 ')
        info = info_temp[0].split(' ')
        install_info['wl_datetime'] = info[-2]+' '+info[-1][:8]
        install_info['wl_status'] = (u'已配置')
    cmd = 'ls -alhG --full-time ' + path + '/openfire.cfg'
    if op_data['op_hostpassword'] != '':
        res = commands.getstatusoutput(cmd)
        info_temp = res[1].split(' +0800 ')
        info = info_temp[0].split(' ')
        install_info['op_datetime'] = info[-2]+' '+info[-1][:8]
        install_info['op_status'] = (u'已配置')
    cmd = 'ls -alhG --full-time ' + path + '/oracle.cfg'
    if or_data['or_hostpassword'] != '':
        res = commands.getstatusoutput(cmd)
        info_temp = res[1].split(' +0800 ')
        info = info_temp[0].split(' ')
        install_info['or_datetime'] = info[-2]+' '+info[-1][:8]
        install_info['or_status'] = (u'已配置')
    cmd = 'ls -alhG --full-time ' + path + '/mysql.cfg'
    if my_data['my_hostpassword'] != '':
        res = commands.getstatusoutput(cmd)
        info_temp = res[1].split(' +0800 ')
        info = info_temp[0].split(' ')
        install_info['my_datetime'] = info[-2]+' '+info[-1][:8]
        install_info['my_status'] = (u'已配置')
    cmd = 'ls -alhG --full-time ' + path + '/fastdfs.cfg'
    if fd_data['fd_hostpassword'] != '':
        res = commands.getstatusoutput(cmd)
        info_temp = res[1].split(' +0800 ')
        info = info_temp[0].split(' ')
        install_info['fd_datetime'] = info[-2]+' '+info[-1][:8]
        install_info['fd_status'] = (u'已配置')
        
    return render_to_response('install.html', install_info, context_instance = RequestContext(request))


def refresh_install(request):
    f = open('/opt/autooption/flag.lock','r')
    info=f.readlines()[0]
    f.close()
    return HttpResponse(json.dumps(info, ensure_ascii = False), mimetype = 'application/json')


def wl_install(request):
    error_info = (u'部署weblogic成功！')
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')


def op_install(request):
    error_info = (u'获取参数失败！')
    print 'start'
    try:
        wl_signal = request.GET['wl_signal']
        op_signal = request.GET['op_signal']
        ol_signal = request.GET['ol_signal']
        my_signal = request.GET['my_signal']
        fd_signal = request.GET['fd_signal']
    except Exception, e:
        print str(e)
        return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')
    print wl_signal, op_signal, ol_signal, my_signal, fd_signal

    for line in os.listdir('/proc'):
        try:
            pid = int(line)
        except ValueError:
            continue
        ff = open('/proc/%d/cmdline' % pid, 'r')
        data = ff.readlines()
        ff.close()
        if 'beanstalkd' in str(data):
            os.kill(pid, 9)
            break

    #subprocess.Popen('/usr/local/bin/beanstalkd &', shell=True)

    #if wl_signal == 'true':
    #    shutil.copyfile('/opt/autooption/autooption/weblogic.cfg', '/opt/autooption/wl_install/weblogic.cfg')
    #    subprocess.Popen('cd /opt/autooption/wl_install && python start.py', shell=True)

    #if op_signal == 'true':
    #    shutil.copyfile('/opt/autooption/autooption/openfire.cfg', '/opt/autooption/op_install/openfire.cfg')
    #    subprocess.Popen('cd /opt/autooption/op_install && python start.py', shell=True)

    #if ol_signal == 'true':
    #    shutil.copyfile('/opt/autooption/autooption/oracle.cfg', '/opt/autooption/ol_install/oracle.cfg')
    #    subprocess.Popen('cd /opt/autooption/ol_install && python start.py', shell=True)

    #if my_signal == 'true':
    #    shutil.copyfile('/opt/autooption/autooption/mysql.cfg', '/opt/autooption/my_install/mysql.cfg')
    #    subprocess.Popen('cd /opt/autooption/my_install && python start.py', shell=True)
    
    #if fd_signal == 'true':
    #    shutil.copyfile('/opt/autooption/autooption/fastdfs.cfg', '/opt/autooption/fd_install/fastdfs.cfg')
    #    subprocess.Popen('cd /opt/autooption/fd_install && python start.py', shell=True)

    ff = open('/opt/autooption/flag.lock', 'w')
    ff.write('00000')
    ff.close()
    error_info = (u'部署成功！')
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')
    
    
def or_install(request):
    error_info = (u'部署oracle成功！')
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')


def ssh_check(request):    
    hostip = request.GET['hostip']
    hostusername = request.GET['hostusername']
    hostpassword = request.GET['hostpassword']
    hostport = request.GET['hostport']

    iplist = hostip.strip().split(' ')
    while '' in iplist:
       iplist.remove('')

    userlist = hostusername.strip().split(' ')
    while '' in userlist:
       userlist.remove('')

    passwdlist = hostpassword.strip().split(' ')
    while '' in passwdlist:
       passwdlist.remove('')

    portlist = hostport.strip().split(' ')
    while '' in portlist:
       portlist.remove('')

    error_info = (u'')
    for eachline in iplist:
        index = iplist.index(eachline)
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
        # connect
        try:
            s = pxssh.pxssh()
            s.login(eachline, hostusername, hostpassword, port=hostport)
            error_info += (u'%s, ssh连接成功！\n' % eachline)
            s.close()
        except Exception:
            error_info += (u'%s, ssh连接失败！\n' % eachline)
    return HttpResponse(json.dumps(error_info, ensure_ascii = False), mimetype = 'application/json')


def monitor(request):
    ipaddr =  request.GET.get('hostip')
    groupname =  request.GET.get('groupname')
    info = {'ipaddr': ipaddr, 'groupname': groupname}
    return render_to_response('monitor.html', info, context_instance = RequestContext(request))


def monitor_data(request):
    ipaddr = request.GET.get('ipaddr')
    sleep =  int(request.GET.get('sleep'))
    now = int(time.time())

    #  init mysql connect
    P = ActuData(ipaddr)

    # cpu data
    tempdata = P.actudata(sleep, 'cpu')
    cpuX = tempdata['dataX']
    cpuY = tempdata['dataY']
    cpuCount = tempdata['cpuCount']

    # cpu wait data
    tempdata = P.actudata(sleep, 'cpuWait')
    cpuWaitX = tempdata['dataX']
    cpuWaitY = tempdata['dataY']

    # mem data
    tempdata = P.actudata(sleep, 'mem')
    memX = tempdata['dataX']
    memY = tempdata['dataY']
    memT = tempdata['memTotal']

    # net data
    tempdata = P.actudata(sleep, 'netOut')
    netOutY = tempdata['dataY']
    netX = tempdata['dataX']

    tempdata = P.actudata(sleep, 'netIn')
    netInY = tempdata['dataY']
    #netInX = tempdata['dataX']
   
    #  disk data
    tmpdata = P.actudata(sleep, 'disk')
    totalSpace = tmpdata['diskT']
    freeSpace = tmpdata['diskfree']
    useSpace = tmpdata['diskuse']
    usePerc = tmpdata['useperc']

    P.close()
    
    info = {'cpuX': cpuX,
            'cpuY': cpuY,
            'cpuCount': cpuCount,
            'cpuWaitX': cpuWaitX,
            'cpuWaitY': cpuWaitY,
            'memX': memX,
            'memY': memY,
            'memT': memT,
            'netX': netX,
            'netOutY': netOutY,
            'netInY': netInY,
            'totalSpace': str(totalSpace) + ' G',
            'freeSpace': str(freeSpace) + ' G',
            'useSpace': str(useSpace) + ' G',
            'usePerc': usePerc}

    return HttpResponse(json.dumps(info, ensure_ascii = False), mimetype = 'application/json')


def history(request):
    ipaddr =  request.GET.get('hostip')
    groupname = request.GET.get('groupname')
    info = {'ipaddr': ipaddr, 'groupname': groupname}
    return render_to_response('history.html', info, context_instance = RequestContext(request))

    
def monitor_historydata(request):
    ipaddr = request.GET.get('ipaddr')
    sleep =  int(request.GET.get('dayCount'))
    datatype = int(request.GET.get('datatype'))

    P = HistData(ipaddr)

    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    timeArray = time.strptime(dt, "%Y-%m-%d")
    now = int(time.mktime(timeArray))
    
    # cpu data
    def cpudata():
        tempdata = P.histdata(sleep, 'cpu')
        cpuY = tempdata['dataY']
        cpuX = tempdata['dataX']
        cpuCount = tempdata['cpuCount']
        message = {'cpuY': cpuY, 'cpuX': cpuX, 'cpuCount': cpuCount}
        return message
        
    # cpu iowait data
    def cpuWaitdata():
        tempdata = P.histdata(sleep, 'cpuWait')
        cpuWaitY = tempdata['dataY']
        cpuWaitX = tempdata['dataX']
        message = {'cpuWaitY': cpuWaitY, 'cpuWaitX': cpuWaitX}
        return message

    # memory data
    def memdata():
        tempdata = P.histdata(sleep, 'mem')
        memY = tempdata['dataY']
        memX = tempdata['dataX']
        memT = tempdata['memTotal']
        message = {'memY': memY, 'memX': memX, 'memT': memT}
        return message

    # network data
    def netOutdata():
        tempdata = P.histdata(sleep, 'netOut')
        netOutY = tempdata['dataY']
        netOutX = tempdata['dataX']
        message = {'netOutY': netOutY, 'netOutX': netOutX}
        return message

    def netIndata():
        tempdata = P.histdata(sleep, 'netIn')
        netInY = tempdata['dataY']
        netInX = tempdata['dataX']
        message = {'netInY': netInY, 'netInX': netInX}
        return message

    # disk data
    def diskdata():
        tempdata = P.histdata(sleep, 'disk')
        diskY = tempdata['dataY']
        diskX = tempdata['dataX']
        diskT = tempdata['diskT']
        message = {'diskY': diskY, 'diskX': diskX, 'diskT': diskT}
        return message

    if datatype == 1:
        info = cpudata()
    elif datatype == 2:
        info = cpuWaitdata()
    elif datatype == 3:
        info = memdata()
    elif datatype == 4:
        info = netIndata()
    elif datatype == 5:
        info = netOutdata()
    else:
        info = diskdata()

    return HttpResponse(json.dumps(info, ensure_ascii = False), mimetype = 'application/json')
    

def watchDATA(request):
    totime = int(time.time())
    ipaddr =  request.GET.get('hostip')

    cpuDict= get_data(ipaddr, u'system.cpu.load[percpu,avg1]', 0, (totime-70), totime)
    cpuList = sorted(cpuDict.keys())[-1]
    cpuUse = str(int(float(cpuDict[cpuList]) * 100))
    
    cpuWaitDict = get_data(ipaddr, u'system.cpu.util[,iowait]', 0, (totime-70), totime)
    cpuWaitList = sorted(cpuWaitDict.keys())[-1]
    cpuWait = cpuWaitDict[cpuWaitList]

    memTDict = get_data(ipaddr, u'vm.memory.size[total]', 3, (totime-3660), totime)
    memTList = sorted(memTDict.keys())[-1]
    memT = memTDict[memTList]

    memDict = get_data(ipaddr, u'vm.memory.size[available]', 3, (totime-70), totime)
    memList = sorted(memDict.keys())[-1]
    memUse = int(float(int(memT)-int(memDict[memList]))/int(memT)*100)

    diskDict = get_data(ipaddr, u'vfs.fs.size[/,pfree]', 0, (totime-70), totime)
    diskList = sorted(diskDict.keys())[-1]
    diskUse = int(100 - float(diskDict[diskList]))

    netOutDict = get_data(ipaddr, u'net.if.out', 3, (totime-70), totime)
    netOutList = sorted(netOutDict.keys())[-1]
    netOutUse = round(int(netOutDict[netOutList])/1000/1000, 1)

    netInDict = get_data(ipaddr, u'net.if.in', 3, (totime-70), totime)
    netInList = sorted(netInDict.keys())[-1]
    netInUse = round(int(netInDict[netInList])/1000/1000, 1)

    info = {
            'cpuUse': cpuUse,
            'cpuWait': cpuWait,
            'memUse': memUse,
            'diskUse': diskUse,
            'netOutUse': netOutUse,
            'netInUse': netInUse
            }
    return HttpResponse(json.dumps(info, ensure_ascii = False), mimetype = 'application/json')
    
##################################################################
def monitor_list(request):
    error_info = ''
    #host = sethost.host_list()
    #group = sethost.group_list()
    #if host == []:
    #    error_info = (u'服务器列表为空！')
    #return render_to_response('host.html', {'error_info':error_info,'host':host, 'group':group}, context_instance = RequestContext(request))
    return render_to_response('monitor_list.html', context_instance = RequestContext(request))


def monitor_get_list(request):
    error_info = ''
    host = sethost.host_list()
    group = sethost.group_list()
    if host == []:
        error_info = (u'服务器列表为空！')
    results = [error_info, host, group]
    return HttpResponse(json.dumps(results, ensure_ascii = False), mimetype = 'application/json')


def monitor_host_add(request):
    error_info = sethost.host_add(request)
    host = sethost.host_list()
    group = sethost.group_list()
    results = [error_info, host, group]
    return HttpResponse(json.dumps(results, ensure_ascii = False), mimetype = 'application/json')

    
#single info
def monitor_singlehost_info(request):
    results = sethost.host_single_info(request)
    return HttpResponse(json.dumps(results, ensure_ascii = False), mimetype = 'application/json')


#single change
def monitor_singlehost_modify(request):
    error_info = sethost.host_single_modify(request)
    host = sethost.host_list()
    group = sethost.group_list()
    results = [error_info, host, group]
    return HttpResponse(json.dumps(results, ensure_ascii = False), mimetype = 'application/json')


def monitor_host_del(request):
    error_info = sethost.host_del(request)
    host = sethost.host_list()
    group = sethost.group_list()
    results = [error_info, host, group]
    return HttpResponse(json.dumps(results, ensure_ascii = False), mimetype = 'application/json')


def monitor_group_add(request):
    error_info = sethost.group_add(request)
    host = sethost.host_list()
    group = sethost.group_list()
    results = [error_info, host, group]
    return HttpResponse(json.dumps(results, ensure_ascii = False), mimetype = 'application/json')


def monitor_group_del(request):
    error_info = sethost.group_del(request)
    host = sethost.host_list()
    group = sethost.group_list()
    results = [error_info, host, group]
    return HttpResponse(json.dumps(results, ensure_ascii = False), mimetype = 'application/json')



def monitor_info(request):
    error_info = ''
    groupname = ''
    try:
        groupname = request.GET['groupname']
    except Exception, e:
        print str(e)
    print '#############groupname='+groupname+'###########'
    info = {'groupname': groupname}    
    return render_to_response('monitor_info.html', info, context_instance = RequestContext(request))


def monitor_get_info(request):
    group = sethost.group_list()
    ret = sethost.monitor_info(request, group)
    error_info = ret[0]
    host = ret[1]
    if host == []:
        error_info = (u'服务器列表为空！')
    results = [error_info, host, group]
    return HttpResponse(json.dumps(results, ensure_ascii = False), mimetype = 'application/json')

#def itop(request):
#    return render_to_response('itop.html', context_instance = RequestContext(request))

@_login_required
def menu(request):
    username = str(request.user)
    password = ''
    try:
        u = User.objects.get(username = username)
        password = str(u.password)
    except Exception, e:
        print e
    encryname = encryuser(username)
    info = {
            'username': username,
            'encryname': encryname,
            'password':password
           }
    return render_to_response('menu.html', info, context_instance = RequestContext(request))

def checklistdata(request):
    message = connect()
    cnn = message[0]
    cursor = message[1]
    query = 'select * from checkshow  order by id desc'
    cursor.execute(query)
    dataList = []
    for i in cursor:
        dataDict = {
                    'id': i[0],
                    'name': '巡检报告(%s)' % str(i[1]),
                    'status': '%s' % i[2]
                   }
        dataList.append(dataDict)
    cursor.close()
    cnn.close()
    #tempDict = {'total': 100, 'rows': dataList}
    return HttpResponse(json.dumps(dataList, ensure_ascii = False), mimetype = 'application/json')

def checklist(request):
    timestamp = 'none'
    ff = open('/etc/crontab', 'r')
    data = ff.readlines()
    ff.close()
    for eachline in data:
        if 'patchReport.py' in eachline:
            tempdata = eachline.split()
            timestamp = '%s:%s' % (tempdata[1], tempdata[0])
    info = {'timestamp': timestamp}
    return render_to_response('checklist.html', info, context_instance = RequestContext(request))


def patchReport(request):
    C = Create(False)
    C.readyaml()
    #return HttpResponse(json.dumps('success', ensure_ascii = False), mimetype = 'application/json')
    #return render_to_response('table1.html', context_instance = RequestContext(request))
    return HttpResponseRedirect('/checklist')

def detail(request):
    filename =  request.GET.get('id').split('(')[-1].split(')')[0]
    message = connect()
    cnn = message[0]
    cursor = message[1]
    query = 'select string from recheck where name="%s"' % filename
    cursor.execute(query)
    dataList = []
    for i in cursor:
        tempdata = base64.b64decode(i[0])
    cursor.close()
    cnn.close()
    info = json.loads(tempdata)
    return render_to_response('detail.html', info, context_instance = RequestContext(request))

def downReport(request):
    filename =  request.GET.get('id').encode('UTF-8').replace(':', '_')
    filenameZip = filename + '.zip'
    if not filenameZip in os.listdir('recheck'):
        patchHtml('%s' % filename)
    
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
 
    the_file_name = 'recheck/%s.zip' % filename
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s.zip"' % filename
    return response

def downExcel(request):
    filename =  request.GET.get('id').encode('UTF-8').split('(')[1].split(')')[0]
    print filename
    
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
 
    the_file_name = u'checkExcel/巡检记录表%s.xls' % filename
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="巡检记录表(%s).xls"' % filename
    return response

def autocheck(request):
    filename =  request.GET.get('timestamp')
    Hour = filename.split(':')[0]
    Min = filename.split(':')[1]
    ff = open('/etc/crontab', 'r')
    data = ff.readlines()
    ff.close()

    flag = False
    ff = open('/etc/crontab', 'w')
    for eachline in data:
        if 'patchReport.py' in eachline:
            ff.write('%s %s * * * root    cd /opt/autooption/autooption && python patchReport.py\n' % (Min, Hour))
            flag = True
            continue
        ff.write(eachline)
    if not flag:
        ff.write('%s %s * * * root    cd /opt/autooption/autooption && python patchReport.py\n' % (Min, Hour))
    ff.close()
    result = ''
    return HttpResponse(result, mimetype = 'application/json')
