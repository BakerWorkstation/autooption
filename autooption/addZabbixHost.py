#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys

from zabbixHostMethod import ManulHost

def create():
    C = ManulHost(sys.argv[2])
    C.addHost('Isphere', sys.argv[1])
    
    # cpu
    C.addTrigger('cpu idle value less than 70%', 'system.cpu.util[,idle]', '<70')

    # mem
    C.addItem('Memory Available Percentage', 'mem.pfree', 3, 7, 60)
    C.addTrigger('Memory Available Percentage < 30%', 'mem.pfree', '<30')
    

    C.addItem('cpu count', 'cpu.count', 3, 7, 60)
    C.addItem('os version', 'os.version', 1, 7, 60)
    C.addItem('web statusCode', 'web.statusCode', 1, 7, 60)
    C.addItem('web cluster status', 'web.cluster', 1, 7, 60)
    C.addItem('item verbose(iptables,selinux ...)', 'item.verbose', 1, 7, 60)
    
    # 获取远程节点硬盘数
    disk = 'sda'
    C.addItem('%s write speed' % disk, 'disk.%s.write' % disk, 3, 7, 30)
    C.addItem('%s read speed' % disk, 'disk.%s.read' % disk, 3, 7, 30)
    C.addTrigger('%s write speed more than 30MB/s' % disk, 'disk.%s.write' % disk, '>30')
    C.addTrigger('%s read speed more than 30MB/s' % disk, 'disk.%s.read' % disk, '>30')

    # login
    C.addTrigger('Number of logged in users > 3','system.users.num', '>3')

    # net
    C.addItem('TCP ESTABLISHED CONNECTION COUNT', 'tcp.count', 3, 7, 60)
    C.addTrigger('TCP ESTABLISHED CONNECTION > 30000', 'tcp.count', '>30000')

    itemdict = C.M.getItem(sys.argv[2])
    for key in itemdict:
        if 'net.if.out' in key:
            name = key.split('[')[-1].split(']')[0]
            C.addTrigger('Outgoing network traffic on %s > 5Mbps' % name, 'net.if.out[%s]' % name, '>5242880')
        if 'net.if.in' in key:
            name = key.split('[')[-1].split(']')[0]
            C.addTrigger('Incoming network traffic on %s > 5Mbps' % name, 'net.if.in[%s]' % name, '>5242880')

    #C.updateItem('disk.sda.write', 30)
    C.updateTrigger('system.cpu.load[percpu,avg1]', '>2')
    C.updateTrigger('system.swap.size[,pfree]', '<20')
    C.updateTrigger('proc.num[]', '>300')
    C.updateTrigger('kernel.maxfiles', '<2048')

if __name__ == '__main__':
    create()
