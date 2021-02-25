#!/usr/bin/env python
#! -*- coding:UTF-8 -*-

import os
import re
import time
import json
import yaml
import base64
import datetime
import threading

import mysql.connector

from Mysql import connect
from excel import PatchExcel
from zabbixHostMethod import ManulHost

class Timer1(threading.Thread):
    def __init__(self, cursor, itemid, ip):
        self.cursor = cursor
        self.itemid = itemid
        self.ip = ip
        threading.Thread.__init__(self)

    def run(self):
        query = 'select clock,value from history_uint where itemid=%s order by clock desc limit 1' % self.itemid
        try:
            self.cursor.execute(query)
            for i in self.cursor:
                timestamp = i[0]
                value = i[1]
        except Exception:
            return
        if int(time.time()) - int(timestamp) < 120:
            if value == 1:
                global alivehost
                alivehost = alivehost + self.ip + ' '
            

class Create(object):

    def __init__(self, flag=True):
        # True: auto;  False: manul
        if flag == True:
            self.typed = '定时巡检'
        elif flag == False:
            self.typed = '手动巡检'
        self.starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.filedir = 'autooption/item/'
            self.files = os.listdir(self.filedir)
        except OSError:
            self.filedir = 'item/'
            self.files = os.listdir(self.filedir)
        for eachfile in self.files:
            if not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', eachfile):
                self.files.remove(eachfile)
        message = connect()
        self.cnn = message[0]
        self.cursor = message[1]

    def close(self):
        self.cursor.close()
        self.cnn.close()

    def readyaml(self):
        data = []
        warnTotal = 0
        disTotal = 0
        commonTotal = 0
        infoTotal = 0
        global alivehost
        alivehost = ''
        successhost = ''
        failhost = ''
        
        
        for eachfile in self.files:
            warnCount = 0
            message = ''
            conffile = '%s%s' % (self.filedir, eachfile)
            ipaddr = eachfile.replace('.yaml', '')
            stream = file(conffile, 'r')
            self.itemdict = yaml.load(stream)
            T = Timer1(self.cursor, self.itemdict['agent.ping'], ipaddr)
            T.start()
            T.join()
            itemlist = ['system.cpu.util[,idle]', 'mem.pfree', 'vfs.fs.size[/,pfree]']
            tablelist = ['history', 'history_uint', 'history']

            for key in itemlist:
                table = tablelist[itemlist.index(key)]
                itemid = self.itemdict[key]
                query = 'select clock,value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                try:
                    self.cursor.execute(query)
                except Exception:
                    continue
                tt = []
                for i in self.cursor:
                    tt.append(i)
                timestamp = tt[0][0]
                value = tt[0][1]
               
                if timestamp > int(time.time()) - 120:
                    usePerc = round(100 - float(value), 1)
                    if itemlist.index(key) == 0:
                        if usePerc > float(10):
                            warnCount += 1
                            message += '%d. CPU使用率超过10%%。_' % warnCount
                    elif itemlist.index(key) == 1:
                        if usePerc > float(10):
                            warnCount += 1
                            message += '%d. 内存使用率超过10%%。_' % warnCount
                    elif itemlist.index(key) == 2:
                        if usePerc > float(10):
                            warnCount += 1
                            message += '%d. 硬盘使用率超过10%%。_' % warnCount
                else:
                    if itemlist.index(key) == 0:
                        warnCount += 1
                        message += '%d. CPU使用率数据获取异常。</br>' % warnCount
                    elif itemlist.index(key) == 1:
                        warnCount += 1
                        message += '%d. 内存使用率数据获取异常。</br>' % warnCount
                    elif itemlist.index(key) == 2:
                        warnCount += 1
                        message += '%d. 硬盘使用率数据获取异常。</br>' % warnCount

            query = 'select value from history_str where itemid=%s order by clock desc limit 1' % (self.itemdict['os.version'])
            try:
                self.cursor.execute(query)
                for i in self.cursor:
                    version = i
            except Exception as e:
                version = ''
            version = str(version[0])
            C = ManulHost(ipaddr)
            info = C.getGroupname()
            groupname = info[0]
            hostname = info[1]
            if not warnCount == 0:
                tempdict = {}
                tempdict['ip'] = ipaddr
                tempdict['hostname'] = hostname
                tempdict['groupname'] = groupname
                tempdict['dis'] = 0
                tempdict['warning'] = warnCount
                tempdict['common'] = 0
                tempdict['system'] = version
                tempdict['discript'] = message
                data.append(tempdict)
            warnTotal += warnCount
        self.stoptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        info = {'info': data}
        result = {
                  'data': json.dumps(info),
                  'starttime': self.starttime,
                  'stoptime': self.stoptime,
                  'type': self.typed,
                  'date': self.date,
                  'disT': 0,
                  'warnT': warnTotal,
                  'commonT': commonTotal,
                  'infoT': infoTotal,
                  'hostCount': len(self.files),
                  'alivehost': alivehost,
                  'successhost': successhost,
                  'failhost': failhost
                 }

        query = "insert into recheck(name, string) values('%s', '%s')" % (self.starttime, base64.b64encode(json.dumps(result)))
        self.cursor.execute(query)
        if not warnTotal == 0:
            status = u'异常'
        else:
            status = u'正常'
        query = "insert into checkshow(name, status) values('%s', '%s')" % (self.starttime, status)
        self.cursor.execute(query)
        self.cnn.commit()
        self.close()
        PatchExcel(self.starttime)

if __name__ == '__main__':
    C = Create(True)
    C.readyaml()
