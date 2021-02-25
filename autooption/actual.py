#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import time
import yaml
import datetime
from Mysql import connect

class ActuData(object):

    def __init__(self, ipaddr):

        conffile = 'autooption/item/%s.yaml' % ipaddr
        stream = file(conffile, 'r')
        self.itemdict = yaml.load(stream)

        message = connect()
        self.cnn = message[0]
        self.cursor = message[1]
         
    def actudata(self, sleep, typeData):
        cpuCount = ''
        memTotal = ''
        dataY = []
        timestamp = int(time.time())
        totime = int(time.time())
        fromtime = totime - 3600 * sleep - 60
        if typeData == 'cpu':
            table = 'history_uint'
            Itemid = self.itemdict['cpu.count']
            query1 = 'select  * from %s where itemid=%s order by clock desc limit 1' % (table, Itemid)
            try:
                self.cursor.execute(query1)
            except Exception:
                pass
            tt = []
            for i in self.cursor:
                tt.append(i)
            try:
                cpuCount = tt[0][2]
            except Exception:
                pass
            itemid = self.itemdict['system.cpu.util[,idle]']
            table = 'history'

        elif typeData == 'cpuWait':
            itemid = self.itemdict['system.cpu.util[,iowait]']
            table = 'history'

        elif typeData == 'netIn':
            for key in self.itemdict:
                if 'net.if.in' in key:
                    itemid = self.itemdict[key]
                    table = 'history_uint'
                    break
            
        elif typeData == 'netOut':
            for key in self.itemdict:
                if 'net.if.out' in key:
                    itemid = self.itemdict[key]
                    table = 'history_uint'
                    break

        elif typeData == 'mem':
            table = 'history_uint'
            Itemid = self.itemdict['vm.memory.size[total]']
            query1 = 'select  * from %s where itemid=%s order by clock desc limit 1' % (table, Itemid)
            self.cursor.execute(query1)
            tt = []
            for i in self.cursor:
                tt.append(i)
            try:
                memT = tt[0][2]
                memTotal = int(round(float(memT)/1024/1024/1024))
            except Exception:
                pass
            itemid = self.itemdict[u'vm.memory.size[available]']

        elif typeData == 'disk':
            table = 'history_uint'
            Itemid = self.itemdict['vfs.fs.size[/,used]']
            query1 = 'select  * from %s where itemid=%s order by clock desc limit 1' % (table, Itemid)
            self.cursor.execute(query1)
            tt = []
            for i in self.cursor:
                tt.append(i)
            diskuse = tt[0][2]
            itemid = self.itemdict[u'vfs.fs.size[/,free]']
            table = 'history_uint'

        query = 'select  * from %s where itemid=%s and clock>= %s and clock<=%s order by clock desc' % (table, itemid, fromtime, totime)
        ntime = datetime.datetime.now().strftime("%H:%M")
        self.cursor.execute(query)
        dataDict={}
        for itemid1 in self.cursor:
            dataDict[itemid1[1]] = itemid1[2]
        dataList = sorted(dataDict.keys(), reverse=True)
        flag = 0
        hour = int(ntime.split(':')[0])
        mint = int(ntime.split(':')[-1])
        oldtime = None
        for eachtime in dataList:
            format1 = '%H:%M'
            eachtime1 = time.localtime(eachtime)
            htime =  time.strftime(format1, eachtime1)
            if oldtime == htime:
                continue
            while 1:
                if len(str(mint)) == 1:
                    mintstr = '0' + str(mint)
                else:
                    mintstr = str(mint)
        
                if len(str(hour)) == 1:
                    hourstr = '0' + str(hour)
                else:
                    hourstr = str(hour) 
        
                if hourstr + ':' + mintstr == htime:
                    if typeData == 'cpu':
                        tempdata = int(round(100 - dataDict[eachtime]))

                    if typeData == 'cpuWait':
                        tempdata = dataDict[eachtime]

                    if typeData == 'mem':
                        tempdata = dataDict[eachtime]
                        tempdata = int(round(float(memT - tempdata)/tempdata*100))

                    if typeData == 'netIn':
                        tempdata = dataDict[eachtime]
                        tempdata = int(round(float(tempdata)/1000/1000, 1))

                    if typeData == 'netOut':
                        tempdata = dataDict[eachtime]
                        tempdata = int(round(float(tempdata)/1000/1000, 1))

                    if typeData == 'disk':
                        diskfree = round(float(dataDict[eachtime])/1024/1024/1024, 1)
                        diskuse = round(float(diskuse)/1024/1024/1024, 1)
                        diskT = diskfree + diskuse
                        useperc =  int(round(float(diskuse)/diskT * 100))
                        message = {'diskT': diskT,
                                   'diskuse': diskuse,
                                   'diskfree': diskfree,
                                   'useperc': useperc}
                        return message


                    flag += 1
                    dataY.insert(0, tempdata)

                    if dataList.index(eachtime) == 0:
                         timestamp = int(time.time())
                    mint -= 1
                    if mint < 0:
                        mint = 59
                        hour -= 1
                        if hour < 0:
                            hour = 23
                    oldtime = htime
                    break
                else:
                    if dataList.index(eachtime) == 0:
                         timestamp = int(time.time())
                    dataY.insert(0, '-')
                    mint -= 1
                    if mint < 0:
                        mint = 59
                        hour -= 1
                        if hour < 0:
                            hour = 23
        
                flag += 1
                if flag > 60 * sleep - 1:
                    break
            if flag > 60 * sleep - 1:
                break
        if len(dataY) < sleep * 60:
            for j in range(1, sleep * 60 - len(dataY) + 1 ):
                dataY.insert(0, '-')
        
        dataX = []
        now = int(timestamp)
        for i in range(0,60 * sleep + 1):
            format1 = '%H:%M'
            eachtime1 = time.localtime(now)
            time1 =  time.strftime(format1, eachtime1)
            dataX.insert(0, time1)
            now -= 60
            
        message = {
                   'dataY': dataY,
                   'dataX': dataX,
                   'cpuCount': cpuCount,
                   'memTotal': memTotal
                   }

        if typeData == 'disk':
            message = {'diskT': 0,
                       'diskuse': 0,
                       'diskfree': 0,
                       'useperc': 0}
        
        return message

    def close(self):
        self.cursor.close()
        self.cnn.close()
