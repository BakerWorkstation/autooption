#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys

from zabbixHostMethod import ManulHost

def create():
    C = ManulHost(sys.argv[2])
    #C.addHost('Isphere', sys.argv[1])
    
    # mem
    C.addItem('Memory Available Percentage', 'mem.pfree', 3, 7, 60)

    C.addItem('cpu count', 'cpu.count', 3, 7, 60)
    C.addItem('os version', 'os.version', 1, 7, 60)
    C.addItem('web statusCode', 'web.statusCode', 1, 7, 60)
    C.addItem('web cluster status', 'web.cluster', 1, 7, 60)
    C.addItem('item verbose(iptables,selinux ...)', 'item.verbose', 1, 7, 60)

    # net
    C.addItem('TCP ESTABLISHED CONNECTION COUNT', 'tcp.count', 3, 7, 60)

if __name__ == '__main__':
    create()
