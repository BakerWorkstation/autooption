#!/user/bin/python
# -*- encoding: UTF-8 -*-

from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.models import User, Permission, Group
from autooption.models import HostList, GroupList
from django.contrib import auth

import time

from zabbix_api import get_data

def host_list():
    error_info = ''
    host = []
    try:
        hostlist = HostList.objects.all()
        print hostlist
    except Exception, e:
        print str(e)
        error_info = (u'服务器列表为空！')        
        return host
    for index, h in enumerate(hostlist):
        hostlist_temp = {}
        hostlist_temp['index'] = index + 1
        hostlist_temp['hostname'] = h.hostname
        hostlist_temp['hostip'] = h.hostip
        hostlist_temp['group'] = h.group
        if h.zabbixagent:
            hostlist_temp['zabbixagent'] = (u'已安装')
        else:
            hostlist_temp['zabbixagent'] = (u'未安装')
        if h.elkagent:
            hostlist_temp['elkagent'] = (u'已安装')
        else:
            hostlist_temp['elkagent'] = (u'未安装')
        hostlist_temp['createdate'] = str(h.createdate)
        host.append(hostlist_temp)
    return host


def host_add(request):
    error_info = (u'添加主机成功！')
    try:
        hostname = request.POST['hostname'].encode('utf-8')
        hostip = request.POST['hostip'].encode('utf-8')
        hostuser = request.POST['hostuser'].encode('utf-8')
        hostpasswd = request.POST['hostpasswd'].encode('utf-8')
        hostport = request.POST['hostport'].encode('utf-8')
        hostgroup = request.POST['hostgroup'].encode('utf-8')
    except Exception, e:
        print str(e)
        error_info = (u'输入非法参数！')
        return error_info
    try:
        host = ''
        host = HostList.objects.get(hostip=hostip)
        print host
    except Exception, e:
        print str(e)
    if host:
        error_info = (u'该主机地址已经存在！')
        return error_info
    HostList.objects.create(hostname=hostname, hostip=hostip, hostuser=hostuser, hostpasswd=hostpasswd, hostport=hostport, group=hostgroup)
    return error_info
    
    
def host_single_info(request):
    error_info = ''
    hostinfo = {}
    try:
        hostip = request.POST['hostip'].encode('utf-8')
    except Exception, e:
        print str(e)
        error_info = (u'输入非法参数！')
        return error_info, hostinfo
    try:
        host = HostList.objects.get(hostip=hostip)
        hostinfo['hostname'] = host.hostname
        hostinfo['hostip'] = host.hostip
        hostinfo['hostuser'] = host.hostuser
        hostinfo['hostpasswd'] = host.hostpasswd
        hostinfo['hostport'] = host.hostport
        hostinfo['hostgroup'] = host.group
    except Exception, e:
        print str(e)
        error_info = (u'获取主机配置信息失败！')
    return error_info, hostinfo
    
    
def host_single_modify(request):
    error_info = (u'修改主机配置信息成功！')
    try:
        hostname = request.POST['hostname'].encode('utf-8')
        hostip = request.POST['hostip'].encode('utf-8')
        hostuser = request.POST['hostuser'].encode('utf-8')
        hostpasswd = request.POST['hostpasswd'].encode('utf-8')
        hostport = request.POST['hostport'].encode('utf-8')
        hostgroup = request.POST['hostgroup'].encode('utf-8')
    except Exception, e:
        print str(e)
        error_info = (u'修改主机配置信息失败！')
        return error_info
    try:
        host = HostList.objects.get(hostip=hostip)
        host.hostname = hostname
        host.hostip = hostip
        host.hostuser = hostuser
        host.hostpasswd = hostpasswd
        host.hostport = hostport
        host.group = hostgroup
        host.save()
    except Exception, e:
        print str(e)
        error_info = (u'修改主机配置信息失败！')
    return error_info
    
    
def host_del(request):
    error_info = (u'删除主机成功！')
    try:
        hostip = request.POST['hostip'].encode('utf-8')
    except Exception, e:
        print str(e)
        error_info = (u'输入非法参数！')
        return error_info
    try:
        host = HostList.objects.get(hostip=hostip)
        print host
        host.delete()
    except Exception, e:
        print str(e)
    return error_info
    
    
def group_list():
    group = []
    try:
        grouplist = GroupList.objects.all()
        print grouplist
    except Exception, e:
        print str(e)
        error_info = (u'服务器列表为空！')        
        return group
    for index, g in enumerate(grouplist):
        group.append(g.group)
    return group


def group_add(request):
    error_info = ('添加组成功！')
    try:
        groupname = request.POST['groupname'].encode('utf-8')
        print groupname
    except Exception, e:
        print str(e)
        error_info = (u'输入非法参数！')
        return error_info
    try:
        g = ''
        g = GroupList.objects.get(group=groupname)
        print g
    except Exception, e:
        print str(e)
    if g:
        error_info = (u'该组已经存在！')
        return error_info
    GroupList.objects.create(group=groupname)
    return error_info
    
    
def group_del(request):
    error_info = ('删除组成功！')
    try:
        groupname = request.POST['groupname'].encode('utf-8')
    except Exception, e:
        print str(e)
        error_info = (u'输入非法参数！')
        return error_info
    try:
        h = ''
        h = HostList.objects.get(group=groupname)
    except Exception, e:
        print str(e)
    if h:
        error_info = (u'该组内主机不为空，禁止删除！')
        return error_info
    try:
        g = GroupList.objects.get(group=groupname)
        print g
        g.delete()
        error_info = (u'删除组成功！')
    except Exception, e:
        print str(e)
        error_info = (u'删除组成功！')
    return error_info


######################global host info
def watchDATA(ipaddr):
    totime = int(time.time())
    #ipaddr =  request.GET.get('hostip')
    
    cpuUse = '-'
    cpuWait = '-'
    memUse = '-'
    diskUse = '-'
    netOutUse = '-'
    netInUse = '-'
    
    try:
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
    except Exception, e:
        print str(e)

    info = {
            'cpuUse': cpuUse,
            'cpuWait': cpuWait,
            'memUse': memUse,
            'diskUse': diskUse,
            'netOutUse': netOutUse,
            'netInUse': netInUse
            }
    return info


def monitor_info(request, group):
    error_info = ''
    host = []
    try:
        groupname = request.POST['groupname'].encode('utf-8')
        print groupname
    except Exception, e:
        print str(e)
        error_info = (u'输入非法参数！')
        return error_info, host
    if not groupname:
        if group:
            groupname = group[0]
        else:
            error_info = (u'服务器列表为空！')
            return error_info, host
    print groupname
    try:
        hostlist = HostList.objects.filter(group=groupname)
        print hostlist
    except Exception, e:
        print str(e)
        error_info = (u'服务器列表为空！')
        return error_info, host
    if not hostlist:
        error_info = (u'服务器列表为空！')
        return error_info, host
    for index, h in enumerate(hostlist):
        hostlist_temp = {}
        hostlist_temp['index'] = index + 1
        hostlist_temp['hostname'] = h.hostname
        hostlist_temp['hostip'] = h.hostip
        hostlist_temp['group'] = h.group
        hostlist_temp['createdate'] = str(h.createdate)
        print h.hostip
        info = watchDATA(str(h.hostip))
        print info
        #TODO: get info from zabbix
        hostlist_temp['alarmcpu'] = info['cpuUse']
        hostlist_temp['alarmmem'] = info['memUse']
        hostlist_temp['alarmdisk'] = info['diskUse']
        hostlist_temp['alarmcpuio'] = info['cpuWait']
        hostlist_temp['alarmnetin'] = info['netInUse']
        hostlist_temp['alarmnetout'] = info['netOutUse']
        
        #TODO: get alarm line from zabbix
        hostlist_temp['linecpu'] = 14
        hostlist_temp['linemem'] = 14
        hostlist_temp['linedisk'] = 14
        hostlist_temp['linecpuio'] = 14
        hostlist_temp['linenetin'] = 14
        hostlist_temp['linenetout'] = 14
        
        host.append(hostlist_temp)
    return error_info, host
    
    
    
    
    
