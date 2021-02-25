#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import yaml
import json
import ConfigParser

import xlwt
from Mysql import connect
import datetime

class PatchExcel(object):

    def __init__(self, filename):
        self.filename = filename
        self.date = datetime.datetime.now().strftime('%H:%M:%S %p')
        self.style()
        self.templet1()
        self.templet2()
        self.templet3()
        
        self.patchdata()
        self.create()
  
    def style(self):
        # sheet 1 style
        self.style1B = xlwt.easyxf('font: height 220,name %s, color-index black, bold on; ' % '微软雅黑'.decode('UTF-8'))
        self.style1D = xlwt.easyxf('font: height 220,name %s, color-index black; ' % '微软雅黑'.decode('UTF-8'))
        self.style3A = xlwt.easyxf('font: height 360,name %s, color-index black, bold on; ' % '宋体(正文)'.decode('UTF-8'))
        self.style4A = xlwt.easyxf('font: name %s, color-index black, bold on; '
                              'pattern: pattern solid, fore_colour aqua;' % '宋体'.decode('UTF-8'))
        self.style12A = xlwt.easyxf('font: height 240,name %s, color-index black, bold on; '
                                    'pattern: pattern solid, fore_colour gray25;' % '宋体'.decode('UTF-8'))
        self.style6B = xlwt.easyxf('font: name %s, color-index black, bold on; '
                              'pattern: pattern solid, fore_colour gray25;' % '宋体'.decode('UTF-8'))
        self.style5C = xlwt.easyxf('font: height 180,name %s, color-index black;' % '宋体'.decode('UTF-8'))
        self.style5CMath = xlwt.easyxf('font: height 180,name %s, color-index black;' % '宋体'.decode('UTF-8'), num_format_str='0%')
        self.wb = xlwt.Workbook()
        self.ws1 = self.wb.add_sheet('基本内容'.decode('UTF-8'))
        #self.ws1.insert_bitmap('1_1.bmp', 0, 0)
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER

        self.style1D.alignment = alignment
        self.style1B.alignment = alignment
        self.style3A.alignment = alignment
        self.style4A.alignment = alignment
        self.style12A.alignment = alignment
        self.style6B.alignment = alignment
        self.style5C.alignment = alignment

        for i in range(0, 8):
            first_col = self.ws1.col(i)
            first_col.width = 256*23

        for j in range(0, 3):
            tall_style = xlwt.easyxf('font:height 400;')
            first_row = self.ws1.row(j)
            first_row.set_style(tall_style)

        for k in range(3, 42):
            tall_style = xlwt.easyxf('font:height 260')
            first_row = self.ws1.row(k)
            first_row.set_style(tall_style)

        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A
        self.style1B.borders = borders
        self.style1D.borders = borders
        self.style3A.borders = borders
        self.style4A.borders = borders
        self.style12A.borders = borders
        self.style6B.borders = borders
        self.style5C.borders = borders
        self.style5CMath.borders = borders

        # sheet 2 style
        self.style0 = xlwt.easyxf('font: name Times New Roman, color-index black , bold on;pattern: pattern solid, fore_colour aqua;',
                         num_format_str='#,##0.00')
        self.style0 = xlwt.easyxf('align: wrap on')
        self.style1 = xlwt.easyxf('font: name Times New Roman, color-index black , bold on',
                         num_format_str='#,##0.00')
        self.style1 = xlwt.easyxf('align: wrap on')
        self.style2 = xlwt.easyxf('font: name Times New Roman, color-index black',
                         num_format_str='#,##0.00')
        self.style2 = xlwt.easyxf('align: wrap on')

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT

        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A

        #pattern0 = xlwt.Pattern()  # Create the Pattern
        #pattern0.pattern = xlwt.Pattern.SOLID_PATTERN
        #pattern0.pattern_fore_colour = 12

        pattern1 = xlwt.Pattern()  # Create the Pattern
        pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern1.pattern_fore_colour = 22

        self.style4A.alignment = alignment
        self.style4A.borders = borders
        #self.style4A.pattern = pattern0

        self.style1.alignment = alignment
        self.style1.borders = borders
        self.style1.pattern = pattern1

        self.style2.alignment = alignment
        self.style2.borders = borders


        self.ws2 = self.wb.add_sheet(u'服务器参数及启动参数')
        '''Line 1'''
        first_col = self.ws2.col(0)
        first_col.width = 256 * 20
        first_col = self.ws2.col(1)
        first_col.width = 256 * 20
        first_col = self.ws2.col(2)
        first_col.width = 256 * 20
        first_col = self.ws2.col(3)
        first_col.width = 256 * 30
        first_col = self.ws2.col(4)
        first_col.width = 256 * 30
        first_col = self.ws2.col(5)
        first_col.width = 256 * 30
        first_col = self.ws2.col(6)
        first_col.width = 256 * 30
        first_col = self.ws2.col(7)
        first_col.width = 256 * 30
        first_col = self.ws2.col(8)
        first_col.width = 256 * 30
        first_col = self.ws2.col(9)
        first_col.width = 256 * 30

        self.ws3 = self.wb.add_sheet(u'安全检查')
        '''Line 1'''
        first_col = self.ws3.col(0)
        first_col.width = 256 * 20
        first_col = self.ws3.col(1)
        first_col.width = 256 * 20
        first_col = self.ws3.col(2)
        first_col.width = 256 * 20
        first_col = self.ws3.col(3)
        first_col.width = 256 * 30
        first_col = self.ws3.col(4)
        first_col.width = 256 * 30
        first_col = self.ws3.col(5)
        first_col.width = 256 * 30
        first_col = self.ws3.col(6)
        first_col.width = 256 * 30


    def templet1(self):
        self.ws1.write(0, 1,
                      '日期：%s'.decode('UTF-8') % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      self.style1B)
        #ws1.write(2, 2, xlwt.Formula("A3+B3"))
        self.ws1.write_merge(0, 0, 3, 7,
                            '注：信息收集周期为第一周的周五至第二周的周四，行业应用提升项目组进行收集信息的汇总'.decode('utf-8'),
                            self.style1D)
        self.ws1.write_merge(1, 2, 0, 7,
                            '即时通讯巡检记录表'.decode('UTF-8'),
                            self.style3A)
        self.ws1.write_merge(3, 3, 0, 2,
                            '服务器'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write(3, 3,
                      '配置'.decode('UTF-8'),
                      self.style4A)
        self.ws1.write(3, 4,
                      '巡检时间'.decode('UTF-8'),
                      self.style4A)
        self.ws1.write(3, 5,
                      'CPU使用率'.decode('UTF-8'),
                      self.style4A)
        self.ws1.write(3, 6,
                      '内存使用率'.decode('UTF-8'),
                      self.style4A)
        self.ws1.write(3, 7,
                      '磁盘使用率'.decode('UTF-8'),
                      self.style4A)
        self.ws1.write_merge(4, 11, 0, 0,
                            '内网服务器'.decode('UTF-8'),
                            self.style12A)
        self.ws1.write_merge(4, 5, 1, 1,
                            '应用服务器'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write_merge(6, 7, 1, 1,
                            '消息服务器'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write_merge(8, 9, 1, 1,
                            '文件服务器'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write_merge(10, 11, 1, 1,
                            '数据库服务器'.decode('UTF-8'),
                            self.style6B)

        self.ws1.write_merge(12, 13, 0, 0,
                            '内网'.decode('UTF-8'),
                            self.style12A)
        self.ws1.write_merge(12, 13, 1, 1,
                            '文件存储'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write(12, 2,
                      '磁盘总量（G）'.decode('UTF-8'),
                      self.style4A)
        self.ws1.write_merge(12, 12, 3, 4,
                            '当日存储量（G）'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write_merge(12, 12, 5, 6,
                            '存储累计使用量（G）'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write(12, 7,
                      '',
                      self.style4A)

        self.ws1.write_merge(14, 26, 0, 0,
                            '数据库情况(用户有DBA权限的进行统计)'.decode('UTF-8'),
                            self.style12A)
        self.ws1.write_merge(14, 15, 1, 1,
                            '表空间情况'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write(14, 2,
                      '表空间总大小（G）'.decode('UTF-8'),
                      self.style4A)
        self.ws1.write_merge(14, 14, 3, 4,
                            '表空间当日使用量（G）'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write_merge(14, 14, 5, 6,
                            '表空间使用量（G）'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write(14, 7,
                      '',
                      self.style4A)
        self.ws1.write_merge(16, 26, 1, 1,
                            '数据库表空间使用情况及表数据数量'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write(16, 2,
                      '数据库表名称'.decode('UTF-8'),
                      self.style4A)
        self.ws1.write_merge(16, 16, 3, 4,
                            '表占空间大小（G）'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write_merge(16, 16, 5, 6,
                            '数据库表名称'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write(16, 7,
                      '',
                      self.style4A)

        self.ws1.write_merge(27, 42, 0, 0,
                            '应用页面情况'.decode('UTF-8'),
                            self.style12A)
        self.ws1.write_merge(27, 31, 1, 1,
                            '应用WEBLOGIC'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write_merge(27, 27, 2, 4,
                            '管理控制台页面'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write_merge(27, 27, 5, 6,
                            '是否正常访问'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write(27, 7,
                      '',
                      self.style4A)
        self.ws1.write_merge(28, 28, 2, 4,
                            'WEBLOGIC管理控制台'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(29, 29, 2, 4,
                            '应用F5 管理控制台'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(30, 30, 2, 4,
                            '应用管理控制台1'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(31, 31, 2, 4,
                            '应用管理控制台2'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(32, 38, 1, 1,
                            '消息OPENFIRE'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write_merge(32, 32, 2, 4,
                            '管理控制台页面'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write_merge(32, 32, 5, 6,
                            '是否正常访问'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write(32, 7,
                      '',
                      self.style4A)
        self.ws1.write_merge(33, 33, 2, 4,
                            'OPENFIRE F5管理控制台'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(34, 34, 2, 4,
                            'OPENFIRE管理控制台1	'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(35, 35, 2, 4,
                            'OPENFIRE1集群状态是否正常'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(36, 36, 2, 4,
                            'OPENFIRE管理控制台2'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(37, 37, 2, 4,
                            'OPENFIRE2集群状态是否正常'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(38, 38, 2, 4,
                            'TCP/IP连接数'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(39, 42, 1, 1,
                            '文件WEBLOGIC'.decode('UTF-8'),
                            self.style6B)
        self.ws1.write_merge(39, 39, 2, 4,
                            '管理控制台页面'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write_merge(39, 39, 5, 6,
                            '是否正常访问'.decode('UTF-8'),
                            self.style4A)
        self.ws1.write(39, 7,
                      '',
                      self.style4A)
        self.ws1.write_merge(40, 40, 2, 4,
                            'WEBLOGIC管理控制台'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(41, 41, 2, 4,
                            'test16页面1'.decode('UTF-8'),
                            self.style5C)
        self.ws1.write_merge(42, 42, 2, 4,
                            'test16页面2'.decode('UTF-8'),
                            self.style5C)

        for row in range(10, 12):
            self.ws1.write(row, 2, '', self.style5C)
            self.ws1.write(row, 3, '', self.style5C)
            self.ws1.write(row, 5, '', self.style5C)
            self.ws1.write(row, 6, '', self.style5C)
            self.ws1.write(row, 7, '', self.style5C)
        for row in [13, 15]:
            self.ws1.write(row, 2, '', self.style5C)
            self.ws1.write_merge(row, row, 3, 4, '', self.style5C)
            self.ws1.write_merge(row, row, 5, 6, '', self.style5C)
            self.ws1.write(row, 7, '', self.style5C)
        for row in range(17, 27):
            self.ws1.write(row, 2, '', self.style5C)
            self.ws1.write_merge(row, row, 3, 4, '', self.style5C)
            self.ws1.write_merge(row, row, 5, 6, '', self.style5C)
            self.ws1.write(row, 7, '', self.style5C)
        for row in range(28, 43):
            if row == 32:
                continue
            elif row == 39:
                continue
            self.ws1.write(row, 7, '', self.style5C)

    def templet2(self):
        self.ws2.write_merge(0, 0, 0, 2, u'服务器', self.style4A)
        self.ws2.write(0, 3, u'字符集', self.style4A)
        self.ws2.write(0, 4, u'文件打开数', self.style4A)
        self.ws2.write(0, 5, u'防火墙是否开启', self.style4A)
        self.ws2.write(0, 6, u'selinux是否开启', self.style4A)
        self.ws2.write(0, 7, u'时钟同步服务器IP', self.style4A)
        self.ws2.write(0, 8, u'是否设置时钟同步服务', self.style4A)
        self.ws2.write(0, 9, u'检测存储挂载是否正常', self.style4A)

        '''Line 2-7'''
        self.ws2.write_merge(1, 6, 0, 0, u'内网服务器', self.style1)
        self.ws2.write_merge(1, 2, 1, 1, u'应用服务器', self.style1)
        self.ws2.write_merge(3, 4, 1, 1, u'消息服务器', self.style1)
        self.ws2.write_merge(5, 6, 1, 1, u'文件服务器', self.style1)
        #self.ws2.write(1, 2, u'节点一', self.style2)
        #self.ws2.write(2, 2, u'节点二', self.style2)
        #self.ws2.write(3, 2, u'节点一', self.style2)
        #self.ws2.write(4, 2, u'节点二', self.style2)
        #self.ws2.write(5, 2, u'节点一', self.style2)
        #self.ws2.write(6, 2, u'节点二', self.style2)

        '''Line 10'''
        self.ws2.write_merge(9, 9, 0, 2, u'服务器', self.style4A)
        self.ws2.write(9, 3, u'启动内存设置值', self.style4A)
        self.ws2.write(9, 4, u'服务器JDK版本', self.style4A)
        self.ws2.write(9, 5, u'openfire系统属性中的 forward.file 和 forward.text 属性值设置是否为 false', self.style4A)
        self.ws2.write_merge(9, 9, 6, 7, u'数据库中以下2张表中是否有数据：oftextforwardaudit，offileforwardaudit', self.style4A)
        self.ws2.write(9, 8, u'日志切割情况', self.style4A)
        self.ws2.write(9, 9, u'数据库连接值', self.style4A)

        '''Line 11-16'''
        self.ws2.write_merge(10, 15, 0, 0, u'内网服务器', self.style1)
        self.ws2.write_merge(10, 11, 1, 1, u'应用服务器', self.style1)
        self.ws2.write_merge(12, 13, 1, 1, u'消息服务器', self.style1)
        self.ws2.write_merge(14, 15, 1, 1, u'文件服务器', self.style1)
        #self.ws2.write(10, 2, u'节点一', self.style2)
        #self.ws2.write(11, 2, u'节点二', self.style2)
        #self.ws2.write(12, 2, u'节点一', self.style2)
        #self.ws2.write(13, 2, u'节点二', self.style2)
        #self.ws2.write(14, 2, u'节点一', self.style2)
        #self.ws2.write(15, 2, u'节点二', self.style2)

        '''Write /'''
        #self.ws2.write(3, 9, '/', self.style2)
        #self.ws2.write(4, 9, '/', self.style2)
        self.ws2.write(10, 5, '/', self.style2)
        self.ws2.write(11, 5, '/', self.style2)
        self.ws2.write(12, 5, '/', self.style2)
        self.ws2.write(13, 5, '/', self.style2)
        self.ws2.write(14, 5, '/', self.style2)
        self.ws2.write(15, 5, '/', self.style2)
        self.ws2.write_merge(10, 10, 6, 7, '/', self.style2)
        self.ws2.write_merge(11, 11, 6, 7, '/', self.style2)
        self.ws2.write_merge(12, 12, 6, 7, '/', self.style2)
        self.ws2.write_merge(13, 13, 6, 7, '/', self.style2)
        self.ws2.write_merge(14, 14, 6, 7, '/', self.style2)
        self.ws2.write_merge(15, 15, 6, 7, '/', self.style2)
        self.ws2.write(14, 8, '/', self.style2)
        self.ws2.write(15, 8, '/', self.style2)
        self.ws2.write(10, 9, '/', self.style2)
        self.ws2.write(11, 9, '/', self.style2)
        self.ws2.write(12, 9, '/', self.style2)
        self.ws2.write(13, 9, '/', self.style2)
        self.ws2.write(14, 9, '/', self.style2)
        self.ws2.write(15, 9, '/', self.style2)
        for row in range(1, 7):
            self.ws2.write(row, 7, '/', self.style2)
            self.ws2.write(row, 8, '/', self.style2)

    def templet3(self):
        self.ws3.write_merge(0, 0, 0, 2, u'服务器', self.style4A)
        self.ws3.write(0, 3, u'JAVA反序列化漏洞是否修复', self.style4A)
        self.ws3.write(0, 4, u'SSRF漏洞是否已修复', self.style4A)
        self.ws3.write(0, 5, u'oracle SCN漏洞补丁是否已修复', self.style4A)
        self.ws3.write(0, 6, u'oracle SCN漏洞补丁修复时间', self.style4A)

        '''Line 2-9'''
        self.ws3.write_merge(1, 8, 0, 0, u'内网服务器', self.style1)
        self.ws3.write_merge(1, 2, 1, 1, u'应用服务器', self.style1)
        self.ws3.write_merge(3, 4, 1, 1, u'消息服务器', self.style1)
        self.ws3.write_merge(5, 6, 1, 1, u'文件服务器', self.style1)
        self.ws3.write_merge(7, 8, 1, 1, u'数据库服务器', self.style1)
        #self.ws3.write(1, 2, u'节点一', self.style2)
        #self.ws3.write(2, 2, u'节点二', self.style2)
        #self.ws3.write(3, 2, u'节点一', self.style2)
        #self.ws3.write(4, 2, u'节点二', self.style2)
        #self.ws3.write(5, 2, u'节点一', self.style2)
        #self.ws3.write(6, 2, u'节点二', self.style2)
        #self.ws3.write(7, 2, u'节点一', self.style2)
        #self.ws3.write(8, 2, u'节点二', self.style2)

        '''Write /'''
        self.ws3.write(3, 3, '/', self.style2)
        self.ws3.write(4, 3, '/', self.style2)
        self.ws3.write(7, 3, '/', self.style2)
        self.ws3.write(8, 3, '/', self.style2)
        self.ws3.write(3, 4, '/', self.style2)
        self.ws3.write(4, 4, '/', self.style2)
        self.ws3.write(7, 4, '/', self.style2)
        self.ws3.write(8, 4, '/', self.style2)
        self.ws3.write(1, 5, '/', self.style2)
        self.ws3.write(2, 5, '/', self.style2)
        self.ws3.write(3, 5, '/', self.style2)
        self.ws3.write(4, 5, '/', self.style2)
        self.ws3.write(5, 5, '/', self.style2)
        self.ws3.write(6, 5, '/', self.style2)
        self.ws3.write(1, 6, '/', self.style2)
        self.ws3.write(2, 6, '/', self.style2)
        self.ws3.write(3, 6, '/', self.style2)
        self.ws3.write(4, 6, '/', self.style2)
        self.ws3.write(5, 6, '/', self.style2)
        self.ws3.write(6, 6, '/', self.style2)
        self.ws3.write(7, 2, '', self.style2)
        self.ws3.write(7, 5, '', self.style2)
        self.ws3.write(7, 6, '', self.style2)
        self.ws3.write(8, 2, '', self.style2)
        self.ws3.write(8, 5, '', self.style2)
        self.ws3.write(8, 6, '', self.style2)
    
    def patchdata(self):
        #path = _get_path()
        config = ConfigParser.ConfigParser()
        #try:
        #    config.read('Isphere.cfg')
        #except:
        try:
            config.read('autooption/Isphere.cfg')
            appS1 = config.get('appserver1-master', 'ip')
            appS2 = config.get('appserver2-slave', 'ip')
            messS1 = config.get('messageserver1-master', 'ip')
            messS2 = config.get('messageserver2-slave', 'ip')
            fileS1 = config.get('fileserver1', 'ip')
            fileS2 = config.get('fileserver2', 'ip')
        except ConfigParser.NoSectionError:
            config.read('Isphere.cfg')
            appS1 = config.get('appserver1-master', 'ip')
            appS2 = config.get('appserver2-slave', 'ip')
            messS1 = config.get('messageserver1-master', 'ip')
            messS2 = config.get('messageserver2-slave', 'ip')
            fileS1 = config.get('fileserver1', 'ip')
            fileS2 = config.get('fileserver2', 'ip')
        #os.system('python addOpenfire.py fileserver1 %s' % fileS1)
        #os.system('python addOpenfire.py fileserver2 %s' % fileS2)
        #os.system('python addWeblogic.py appserver1 %s' % appS1)
        #os.system('python addWeblogic.py appserver2 %s' % appS2)
        #os.system('python addWeblogic.py messageserver1 %s' % messS1)
        #os.system('python addWeblogic.py messageserver2 %s' % messS2)
        ipList = []
        ipList.append(appS1)
        ipList.append(appS2)
        ipList.append(messS1)
        ipList.append(messS2)
        ipList.append(fileS1)
        ipList.append(fileS2)
        message = connect()
        self.cnn = message[0]
        self.cursor = message[1]
        flag_i = 4
        flag_j = 1
        flag_k = 0
        for eachip in ipList:
            try:
                stream = file('item/%s.yaml' % eachip, 'r')
            except IOError:
                stream = file('autooption/item/%s.yaml' % eachip, 'r')
            self.itemdict = yaml.load(stream)
            # cpu
            itemid = self.itemdict['cpu.count']
            table = 'history_uint'
            query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
            self.cursor.execute(query)
            for i in self.cursor:
                cpuCount = i[0]
            # mem
            itemid = self.itemdict['vm.memory.size[total]']
            table = 'history_uint'
            query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
            self.cursor.execute(query)
            for i in self.cursor:
                memTotal = int(round(float(i[0])/1024/1024/1024))
            # disk
            itemid = self.itemdict['vfs.fs.size[/,total]']
            table = 'history_uint'
            query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
            self.cursor.execute(query)
            for i in self.cursor:
                diskTotal = int(round(float(i[0])/1024/1024/1024))
            # cpu percentage
            itemid = self.itemdict['system.cpu.util[,idle]']
            table = 'history'
            query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
            self.cursor.execute(query)
            for i in self.cursor:
                cpuPerc = round((100 - float(i[0]))/100, 2)
            # mem percentage
            itemid = self.itemdict['mem.pfree']
            table = 'history_uint'
            query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
            self.cursor.execute(query)
            for i in self.cursor:
                memPerc = round(float(100 - int(i[0]))/100, 2)
            # disk percentage
            itemid = self.itemdict['vfs.fs.size[/,pfree]']
            table = 'history'
            query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
            self.cursor.execute(query)
            for i in self.cursor:
                diskPerc = round(float(100 - int(i[0]))/100, 2)
            self.ws1.write(flag_i, 2, eachip, self.style5C)
            self.ws1.write(flag_i, 3, '%sC\%sG\%sG'% (cpuCount, memTotal, diskTotal), self.style5C)
            self.ws1.write(flag_i, 5, cpuPerc, self.style5CMath)
            self.ws1.write(flag_i, 6, memPerc, self.style5CMath)
            self.ws1.write(flag_i, 7, diskPerc, self.style5CMath)
            flag_i += 1
            # itemverbose                
            itemid = self.itemdict['item.verbose']
            table = 'history_str'
            query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
            self.cursor.execute(query)
            for i in self.cursor:
                tempitem = str(i[0])
           
            iteminfo = json.loads(tempitem)
            self.ws2.write(flag_j, 2, eachip, self.style5C)
            self.ws2.write(flag_j, 3, iteminfo['character'], self.style5C)
            self.ws2.write(flag_j, 4, int(iteminfo['ulimit']), self.style5C)
            self.ws2.write(flag_j, 5, iteminfo['iptables'], self.style5C)
            self.ws2.write(flag_j, 6, iteminfo['selinux'], self.style5C)
            self.ws2.write(flag_j, 9, iteminfo['storage'], self.style5C)

            self.ws2.write((flag_j + 9), 2, eachip, self.style5C)
            self.ws2.write((flag_j + 9), 3, iteminfo['memStart'], self.style5C)
            self.ws2.write((flag_j + 9), 4, iteminfo['jdkVersion'], self.style5C)
            flag_j += 1

            
            tempdict = ''
            if flag_k == 0:
                itemid = self.itemdict['wl.polling']
                table = 'history_str'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    wlPolling = i[0]
                tempdict = json.loads(str(wlPolling))
                self.ws1.write_merge(28, 28, 5, 6, u'%s' % tempdict['console'], self.style5C)
                self.ws1.write_merge(29, 29, 5, 6, tempdict['IMPotalServerP2'], self.style5C)
                self.ws1.write_merge(30, 30, 5, 6, tempdict['IMPotalServerP2'], self.style5C)
                self.ws2.write(10, 8, tempdict['WlLog'], self.style5C)
                self.ws3.write(1, 2, eachip, self.style5C)
                self.ws3.write(1, 3, tempdict['JRS'], self.style5C)
                self.ws3.write(1, 4, tempdict['SSRF'], self.style5C)
            elif flag_k == 1:
                itemid = self.itemdict['wl.polling']
                table = 'history_str'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    wlPolling = i[0]
                tempdict = json.loads(str(wlPolling))
                self.ws1.write_merge(31, 31, 5, 6, tempdict['IMPotalServerP2'], self.style5C)
                self.ws2.write(11, 8, tempdict['WlLog'], self.style5C)
                self.ws3.write(2, 2, eachip, self.style5C)
                self.ws3.write(2, 3, tempdict['JRS'], self.style5C)
                self.ws3.write(2, 4, tempdict['SSRF'], self.style5C)
            elif flag_k == 2:
                itemid = self.itemdict['wl.polling']
                table = 'history_str'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    wlPolling = i[0]
                tempdict = json.loads(str(wlPolling))
                self.ws1.write_merge(40, 40, 5, 6, tempdict['console'], self.style5C)
                self.ws1.write_merge(41, 41, 5, 6, tempdict['test16'], self.style5C)
                self.ws2.write(12, 8, tempdict['WlLog'], self.style5C)
                self.ws3.write(3, 2, eachip, self.style5C)
                self.ws3.write(5, 3, tempdict['JRS'], self.style5C)
                self.ws3.write(5, 4, tempdict['SSRF'], self.style5C)
            elif flag_k == 3:
                itemid = self.itemdict['wl.polling']
                table = 'history_str'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    wlPolling = i[0]
                tempdict = json.loads(str(wlPolling))
                self.ws1.write_merge(42, 42, 5, 6, tempdict['test16'], self.style5C)
                self.ws2.write(13, 8, tempdict['WlLog'], self.style5C)
                self.ws3.write(4, 2, eachip, self.style5C)
                self.ws3.write(6, 3, tempdict['JRS'], self.style5C)
                self.ws3.write(6, 4, tempdict['SSRF'], self.style5C)
            elif flag_k == 4:
                itemid = self.itemdict['web.cluster']
                table = 'history_str'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    flagCluster = i[0]
                self.ws1.write_merge(33, 33, 5, 6, str(flagCluster), self.style5C)
                self.ws1.write_merge(34, 34, 5, 6, str(flagCluster), self.style5C)
                self.ws3.write(5, 2, eachip, self.style5C)
                
                itemid = self.itemdict['web.statusCode']
                table = 'history_str'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    statusCode = i[0]
                self.ws1.write_merge(35, 35, 5, 6, str(statusCode), self.style5C)

                itemid = self.itemdict['tcp.count']
                table = 'history_uint'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    tcpCount = i[0]
                self.ws1.write(38, 5, tcpCount, self.style5C)
            elif flag_k == 5:
                itemid = self.itemdict['web.cluster']
                table = 'history_str'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    flagCluster = i[0]
                self.ws1.write_merge(36, 36, 5, 6, str(flagCluster), self.style5C)
                self.ws3.write(6, 2, eachip, self.style5C)
                
                itemid = self.itemdict['web.statusCode']
                table = 'history_str'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    statusCode = i[0]
                self.ws1.write_merge(37, 37, 5, 6, str(statusCode), self.style5C)

                itemid = self.itemdict['tcp.count']
                table = 'history_uint'
                query = 'select value from %s where itemid=%s order by clock desc limit 1' % (table, itemid)
                self.cursor.execute(query)
                for i in self.cursor:
                    tcpCount = i[0]
                self.ws1.write(38, 6, tcpCount, self.style5C)

            flag_k += 1

        self.ws1.write_merge(4, 5, 4, 4, self.date, self.style5C)
        self.ws1.write_merge(6, 7, 4, 4, self.date, self.style5C)
        self.ws1.write_merge(8, 9, 4, 4, self.date, self.style5C)
        self.ws1.write_merge(10, 11, 4, 4, self.date, self.style5C)

        
    def create(self):
        try:
            self.wb.save(u'checkExcel/巡检记录表%s.xls' % self.filename)
        except IOError:
            self.wb.save(u'../checkExcel/巡检记录表%s.xls' % self.filename)

if __name__ == '__main__':
    P = PatchExcel('asdasd')
