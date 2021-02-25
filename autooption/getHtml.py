#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import urllib
import shutil
import zipfile

def patchHtml(filename):
    def reporthook(blocks_read, block_size, total_size):
        if not blocks_read:
            #print '打开连接'
            return
        if total_size < 0:
            #print "%d正在读取(%dbytes完成)"%(blocks_read, blocks_read * block_size)
            pass
        else:
            amout_read = block_size * blocks_read
            #print '%d正在读取，%d/%d'%(blocks_read, amout_read, total_size)
            return
    try:
        fileName, msg = urllib.urlretrieve('http://127.0.0.1:8000/detail/?id=%s' % filename.replace('_', ':'), '%s.html' % filename, reporthook=reporthook)
        #print
        #print '文件是：', filename
        #print '头文件是'
        #print msg
        #print '删除前的文件地址：', os.path.exists(filename)
    finally:
        urllib.urlcleanup()
        #print '文件依然存在：', os.path.exists(filename)
    #filename = filename.replace(':', '-')
    ff = open('%s' % fileName, 'rb')
    data = ff.readlines()
    ff.close()
  
    fileName = fileName.replace(':', '-')
    ff = open('%s' % fileName, 'wb')
    for eachline in data:
        if '/static/menu/' in eachline:
             eachline = eachline.replace('/static/menu', '%s_files' % filename)
        ff.write(eachline)
    ff.close()
     
    filedir = '%s_files' % filename
    cssdir = os.path.join(filedir, 'css')
    jsdir = os.path.join(filedir, 'js')
    imagesdir = os.path.join(filedir, 'images')
    os.mkdir(filedir)
    os.mkdir(cssdir)
    os.mkdir(jsdir)
    os.mkdir(imagesdir)
    shutil.copyfile('static/menu/css/bootstrap-combined.min.css', '%s/bootstrap-combined.min.css' % cssdir)
    shutil.copyfile('static/menu/css/bootstrap.min.css', '%s/bootstrap.min.css' % cssdir)
    shutil.copyfile('static/menu/js/jquery-3.2.0.js', '%s/jquery-3.2.0.js' % jsdir)
    shutil.copyfile('static/menu/js/bootstrap.min.js', '%s/bootstrap.min.js' % jsdir)
    shutil.copyfile('static/menu/js/echarts-all.js', '%s/echarts-all.js' % jsdir)
    shutil.copyfile('static/menu/images/minus.gif', '%s/minus.gif' % imagesdir)
    shutil.copyfile('static/menu/images/plus.gif', '%s/plus.gif' % imagesdir)

 
    f = zipfile.ZipFile('recheck/%s.zip' % filename,'w', zipfile.ZIP_DEFLATED) 
    startdir = filedir 
    for dirpath, dirnames, filenames in os.walk(startdir): 
        for filename in filenames: 
            f.write(os.path.join(dirpath,filename)) 
    f.write(fileName)
    f.close()

    shutil.rmtree(filedir)
    os.remove(fileName)
