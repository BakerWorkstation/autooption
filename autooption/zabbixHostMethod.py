#!/usr/bin/env python

import os
import yaml

from zabbix_api import ManulZabbix


class ManulHost(object):

    def __init__(self, ipaddr):
        try:
            zabbixconf = 'autooption/item/zabbix.yaml'
            stream = file(zabbixconf, 'r')
        except IOError:
            zabbixconf = './item/zabbix.yaml'
            stream = file(zabbixconf, 'r')
        self.ipaddr = ipaddr
        config = yaml.load(stream)
        ip = config['host']
        username = 'Admin'
        password = 'zabbix'
        self.M = ManulZabbix(ip, username, password)
        self.M.getHostid(self.ipaddr)

    def addGroup(self, groupname):
        info = self.M.create_hostgroup(groupname)
        if info == "'result'":
            print 'group exist'

    def getGroupid(self, groupname):
        self.M.group_id(groupname)

    def getTemplateId(self, templatename):
        self.M.template_id(templatename)
       
    def addHost(self, groupname , hostname, template='Template OS Linux'):
        self.addGroup(groupname)
        self.getGroupid(groupname)
        self.getTemplateId(template)
        info = self.M.create_host(hostname, self.ipaddr)
        if info == "'result'":
            print 'ip address exist'
        self.M.getHostid(self.ipaddr)

    def addItem(self, name, key, valueType, history, delay):
        self.M.getHostid(self.ipaddr)
        self.M.getInterfaceid()
        # valueType
        # 0: float  1: str  2: log  3: uint  4: text
        info = self.M.createItem(name, key, valueType, history, delay)
        if info == "'result'":
            print 'item exist'
        self.M.getItem(self.ipaddr)
 
    def updateItem(self, item, value):
        self.M.getItem(self.ipaddr)
        self.M.updateItem(item, value)
        self.M.getItem(self.ipaddr)
        
    def addTrigger(self, description, key, manul):
        info = self.M.createTrigger(description, key, manul)
        if info == "'result'":
            print 'trigger exist'

    def updateTrigger(self, key, manul):
        self.M.getTriggerid()
        itemdict = self.M.getItem(self.ipaddr)
        try:
            itemid = itemdict[key]
        except TypeError:
            print 'no such trigger'
            return 
        triggerdict = self.M.trigger
        try:
            triggerid = triggerdict[itemid]
        except KeyError:
            print 'no such trigger'
            return 
        expression = '{%s:%s.last(0)}%s' % (self.M.hostname, key, manul)
        self.M.updateTrigger(triggerid, expression)

    def getAlert(self):
        for eachline in self.M.getAlert():
            print eachline['description']
 
    def getGroupname(self):
        return (self.M.getGroupname(self.ipaddr), self.M.hostname)


if __name__ =='__main__':
    C = ManulHost('172.17.78.89')
    C.getGroupname()

#    C.addHost('Isphere_test', 'message')
#    C.addItem('sda write speed', 'disk.sda.write', 3, 7, 30)
#    C.updateItem('disk.sda.write', 60)
#    C.addTrigger('sda write speed more than 10MB/s', 'disk.sda.write', '>10')
#    C.updateTrigger('disk.sda.write', '>20')
    #C.addTrigger('sda write speed more than 10MB/s', 'disk.sda.write', '>10')
    #C.addItem('sda write speed', 'disk.sda.write', 3, 7, 30)
    #C.addItem('sda read speed', 'disk.sda.read', 3, 7, 30)
    #C.addTrigger('sda read speed more than 10MB/s', 'disk.sda.read', '>10')
#    C.getAlert()
