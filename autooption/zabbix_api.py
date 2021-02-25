#!/usr/bin/env python
# -*- coding:UTF-8 -*-

__author__ = 'BurNing'
__date__ = '2017/02/13'


import time
import yaml
import json
import urllib2

class ManulZabbix():
    
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.login()

    def api_manul(self, data):
        # based url and required header
        url = "http://%s/zabbix/api_jsonrpc.php" % self.ip
        header = {"Content-Type": "application/json"}
        # auth user and password
        jsondata = json.dumps(data)
        # create request object
        request = urllib2.Request(url,jsondata)
        for key in header:
            request.add_header(key,header[key])
            # auth and get authid
        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
            #print response
            message = response['result']
            return message
        except Exception as e:
            return str(e)
            #print "Auth Failed, Please Check Your Name And Passwor:"

    def login(self):
        data = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                           "user": self.username,
                           "password": self.password},
                "id": 0}
        self.cookie = self.api_manul(data)
        #print self.cookie

    def create_hostgroup(self, groupname):
        data = {
                "jsonrpc": "2.0",
                "method": "hostgroup.create",
                "params": {
                           "name": groupname},
                           "auth": self.cookie,
                           "id": 1}
        return self.api_manul(data)

    def group_id(self, groupname):
        data = {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                           "output": "extend",
                           "filter": {
                                      "name": groupname}},
                           "auth": self.cookie,
                           "id": 1}
        #print self.api_manul(data)
        self.groupid = self.api_manul(data)[0]['groupid']

    def template_id(self, template):
        data = {
                "jsonrpc": "2.0",
                "method": "template.get",
                "params": {
                           "output": "extend",
                           "filter": {"host": template}},
                "auth": self.cookie,
                "id": 1}
        self.templateid = self.api_manul(data)[0]['templateid']
   
    def create_host(self, hostname, ip):
        data = {
                 "jsonrpc": "2.0",
                 "method": "host.create",
                 "params":{
                           "host": hostname,
                           "interfaces":[
                                         {"type": 1,
                                         "main": 1,
                                         "useip": 1,
                                         "ip": ip,
                                         "dns": "",
                                         "port": "10050"}],
                           "groups": [{
                                       "groupid": self.groupid}],
                           "templates": [{
                                          "templateid": self.templateid}]},
                 "auth": self.cookie,
                 "id": 1}
        return self.api_manul(data)

    def getHostid(self, ipaddr):
        data = {
                "jsonrpc": "2.0",
                "method": "hostinterface.get",
                "params": {
                           "output": "extend"},
                "auth": self.cookie,
                "id": 1}
        for eachline in self.api_manul(data):
            if eachline['ip'] == ipaddr:
                self.hostid = eachline['hostid']
                break
        self.get_hostname()

    def getGroupname(self, ipaddr):
        self.getHostid(ipaddr)
        data = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                           "output": ["hostid"],
                           "selectGroups": "extend",
                           "filter": {
                                      "hostid": [
                                               self.hostid
                                              ]
                                     }
                          },
                "auth": self.cookie,
                "id": 2
               }
        return self.api_manul(data)[0]['groups'][0]['name']
 
    def get_hostname(self):
        try:
            data = {
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                               "output": "extend",
                               "filter": {
                                          "hostid": self.hostid}},
                    "auth": self.cookie,
                    "id": 1}
        except AttributeError:
            print '\n\033[31mMessage: no such ip address!\033[0m\n'
            return
        self.hostname = self.api_manul(data)[0]['host']

    def getItem(self, host):
        try:
            data = {
                    "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                               "output": "extend",
                               "hostids": self.hostid,
                               "search": {
                                          #"key_": "system"
                                          },
                               "sortfield": "name"},
                    "auth": self.cookie,
                    "id": 1}
        except AttributeError:
            return
        self.item = {}
        string = ''
        for i in self.api_manul(data):
            
            key = i['key_']
            value = i['itemid']
            self.item[key] = value
            string = string + key + ': ' + value + '\n'
        string = '''%s''' % string
        try:
            stream = file('autooption/item/%s.yaml' % host,'w')
        except IOError:
            stream = file('./item/%s.yaml' % host,'w')

        yaml.dump(yaml.load(string), stream)
        #print self.item

        return self.item

    def updateItem(self, item, time):
        try:
            data = {
                    "jsonrpc": "2.0",
                    "method": "item.update",
                    "params": {
                               "hostids": self.hostid,
                               "itemid": self.item[item],
                               "delay": time},
                    "auth": self.cookie,
                    "id": 1}
        except AttributeError:
            print 'no such item'
            return
        except KeyError:
            print 'no such item'
            return
        self.api_manul(data)

    def getInterfaceid(self):
        data = {
                "jsonrpc": "2.0",
                "method": "hostinterface.get",
                "params": {
                           "output": "extend",
                           "hostids": self.hostid},
                "auth": self.cookie,
                "id": 1}
        self.interfaceid = self.api_manul(data)[0]['interfaceid']

    def createItem(self, name, key , valueType, history, delay):
        data = {
                "jsonrpc": "2.0",
                "method": "item.create",
                "params": {
                           "name": name,
                           "key_": key,
                           "hostid": self.hostid,
                           "type": 0,
                           "value_type": valueType,
                           "interfaceid": self.interfaceid,
                           "history": history,
                           "delay": delay},
                "auth": self.cookie,
                "id": 1}
        return self.api_manul(data)
        
    def getTriggerid(self):
        try:
            data = {
                    "jsonrpc": "2.0",
                    "method": "trigger.get",
                    "params": {
                               "output": "extend",
                               "hostids": self.hostid,
                               "selectFunctions": "extend"},
                    "auth": self.cookie,
                    "id": 1}
        except AttributeError:
            return
        self.trigger = {}
        for j in self.api_manul(data):
            key = j['functions'][0]['itemid']
            value = j['functions'][0]['triggerid']
            self.trigger[key] = value
        
    def createTrigger(self, description, key, manul):
        data = {
                "jsonrpc": "2.0",
                "method": "trigger.create",
                "params": {
                           "description": description,
                           "expression": "{%s:%s.last(0)}%s" % (self.hostname, key, manul),
                           "priority": 2,
                           "status": 0},

                "auth": self.cookie,
                "id": 1}
        return self.api_manul(data)

    def updateTrigger(self, triggerid, expression):
        data = {
                "jsonrpc": "2.0",
                "method": "trigger.update",
                "params": {
                           "triggerid": triggerid,
                           "expression": expression},
                "auth": self.cookie,
                "id": 1}
        self.api_manul(data)

    def getAlert(self):
        data = {
                "jsonrpc": "2.0",
                "method": "trigger.get",
                "params": {
                           "hostids": self.hostid,
                           "output": [
                                      "triggerid",
                                      "description",
                                      "priority"],
                           "filter": {
                                      "value": 1},
                           "sortfield": "priority",
                           "sortorder": "DESC"},
                "auth": self.cookie,
                "id": 1}
        return self.api_manul(data)

    #def history_get(self, itemid, i, fromtime, totime):
    def history_get(self, itemid, i, fromtime, totime):
        data = {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                           "output": "extend",
                           "history": i,
                           "itemids": self.item[itemid],
                           "sortfield": "clock",
                           "sortorder": "DESC",
                           "hostids": self.hostid,
                           "time_from": fromtime,
                           "time_till": totime},
                "auth": self.cookie,
                "id": 1}
        tmpdata = {}
        for i in  self.api_manul(data):
            tmpdata[int(i['clock'])] = i['value']
        return tmpdata

def get_data(host, key, flag, fromtime, totime):
    M = ManulZabbix('172.17.78.91', 'Admin', 'zabbix')

    #M.create_hostgroup('Isphere')
    #M.group_id('Isphere')
    #M.template_id('Template OS Linux')
    #M.create_host('fileserver1', '172.17.78.89')

    M.getHostid(host) # ipaddr
    item = M.getItem(host)
    #M.updateItem('agent.version', 100)
    #M.getInterfaceid()
    #M.createItem()

    #M.getTigger()
    #M.createTigger()

    #M.history_get(u'vfs.fs.size[/,total]', 3, 3600)
    if key == u'net.if.out':
        for eachitem in item:
            if key in eachitem:
                key = eachitem
                break
            if 'net.if.out' in eachitem:
                key = eachitem
                break
    if key == u'net.if.in':
        for eachitem in item:
            if key in eachitem:
                key = eachitem
                break
            if 'net.if.in' in eachitem:
                key = eachitem
                break
    return M.history_get(key, flag, fromtime, totime)

if __name__ == '__main__':
    totime = int(time.time())
    fromtime = totime - 3600 
    #print len(get_data('172.17.78.89', u'system.cpu.load[percpu,avg1]', 0, fromtime, totime))

    M = ManulZabbix('172.17.78.91', 'Admin', 'zabbix')
    #M.getHostid(host) # ipaddr
    #item = M.getItem(host)
    M.getGroupname('172.17.78.89')
    #print get_data('172.17.78.89', u'system.cpu.load[percpu,avg1]', 0, fromtime, totime)

    #get_data('172.17.78.89', u'vm.memory.size[total]', 3, fromtime, totime)
    #print len(get_data('172.17.78.89', u'vm.memory.size[available]', 3, fromtime, totime))

#    get_data('172.17.78.89', u'net.if.in', 3, fromtime, totime)
#    get_data('172.17.78.89', u'net.if.out', 3, fromtime, totime)

    #print get_data(u'172.17.78.89', u'vfs.fs.size[/,total]', 3, fromtime, totime).values()
    #args = ['a', 'b', 'c']
    #get_data(u'172.17.78.89', u'vfs.fs.size[/,free]', 3, fromtime, totime)
    #get_data(u'172.17.78.89', u'vfs.fs.size[/,free]', 3, fromtime, totime)
    #print get_data(u'172.17.78.89', u'vfs.fs.size[/,pfree]', 0, fromtime, totime).values()
    #print len(get_data(u'172.17.78.89', u'vfs.fs.size[/,used]', 3, fromtime, totime).values())

