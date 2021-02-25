#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import time
import yaml
import datetime
from Mysql import connect

class HistData(object):

    def __init__(self, ipaddr):
        conffile = 'autooption/item/%s.yaml' % ipaddr
        stream = file(conffile, 'r')
        self.itemdict = yaml.load(stream)

        message = connect()
        self.cnn = message[0]
        self.cursor = message[1]

    def histdata(self, day, typeData):
        cpuCount = ''
        memTotal = ''
        diskT = ''
        today = datetime.date.today() 
        yesterday = today.strftime("%Y-%m-%d %H:%M:%S")
        timeArray = time.strptime(yesterday, "%Y-%m-%d %H:%M:%S")
        #flag = 60 * sleep * day + 1
        dataY = []
        for i in range(1, day+1):
            totime = int(time.mktime(timeArray)) - (i-1) * 3600 * 24
            fromtime = totime - 3600 * 24
            flag = 60 * 24 
            ntime = '23:59'
    
            if typeData == 'cpu':
                table = 'history_uint'
                Itemid = self.itemdict['cpu.count']
                query1 = 'select  * from %s where itemid=%s order by clock desc limit 1' % (table, Itemid)
                self.cursor.execute(query1)
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
                query1 = 'select  * from %s where itemid=%s and clock>= %s and clock<%s order by clock desc' % (table, Itemid, fromtime, totime)
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
                try:
                    diskuse = tt[0][2]
                except Exception:
                    diskuse = ''
                Itemid = self.itemdict['vfs.fs.size[/,free]']
                query2 = 'select  * from %s where itemid=%s order by clock desc limit 1' % (table, Itemid)
                self.cursor.execute(query2)
                tt = []
                for i in self.cursor:
                    tt.append(i)
                try:
                    diskfree = tt[0][2]
                except Exception:
                    diskfree = ''
                diskT = round(float(diskfree + diskuse)/1024/1024/1024, 1)

                itemid = self.itemdict[u'vfs.fs.size[/,pfree]']
                table = 'history'
    
            query = 'select  * from %s where itemid=%s and clock>= %s and clock<%s order by clock desc' % (table, itemid, fromtime, totime)
            self.cursor.execute(query)
            dataDict={}
            for itemid1 in self.cursor:
                dataDict[itemid1[1]] = itemid1[2]
    
            dataList = sorted(dataDict.keys(), reverse=True)
            dataYList = []
            dataYListtemp = []
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
                        elif typeData == 'cpuWait':
                            tempdata = dataDict[eachtime]
                        elif typeData == 'mem':
                            tempdata = dataDict[eachtime]
                            tempdata = int(round(float(memT - tempdata)/tempdata*100))
                        elif typeData == 'netIn':
                            tempdata = dataDict[eachtime]
                            tempdata = int(round(float(tempdata)/1000/1000, 1))
                        elif typeData == 'netOut':
                            tempdata = dataDict[eachtime]
                            tempdata = int(round(float(tempdata)/1000/1000, 1))
                        elif typeData == 'disk':
                            tempdata = dataDict[eachtime]
                            tempdata = int(round(100 - float(tempdata)))
                        dataYListtemp.insert(0, tempdata)
                        flag += 1
    
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
                        dataYListtemp.insert(0, '-')
                        mint -= 1
                        if mint < 0:
                            mint = 59
                            hour -= 1
                            if hour < 0:
                                hour = 23
            
                    flag += 1
                    if flag > 1439:
                        break
                if flag > 1439:
                    break
            if len(dataYListtemp) < 1440:
                for j in range(1, 1440 - len(dataYListtemp) + 1 ):
                    dataYListtemp.insert(0, '-')
            
            index = 0
            while index < len(dataYListtemp):
                dataYList.append(dataYListtemp[index])
                index += 10
            dataY.append(dataYList)
                
        dataX = []
        flag = 0
        for i in range(0,24):
            for j in range(0,60):
                i = str(i)
                j = str(j)
                if len(i) == 1:
                    i = '0' + str(i)
                if len(j) == 1:
                    j = '0' + str(j)
                if flag == 0:
                    timestamp = i + ':' + j
                    dataX.append(timestamp)
                    flag = 10
                flag -= 1
        message = {
                   'dataY': dataY,
                   'dataX': dataX,
                   'cpuCount': cpuCount,
                   'memTotal': memTotal,
                   'diskT': diskT
                   }

        self.close()
        return message

    def close(self):
        self.cursor.close()
        self.cnn.close()
