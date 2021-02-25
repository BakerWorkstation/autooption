#!/usr/bin/env python

import logging  
  
class Logrecord(object):


    def __init__(self, ip):
        self.ip = ip
        self.format()

    def format(self):
        self.logger = logging.getLogger('%s' % self.ip)
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler('./remote_install/logs/%s_log' % self.ip, mode='a')
        formatter = logging.Formatter('%(asctime)s    %(levelname)s    %(name)s    %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
      
    def info(self, info):
        self.logger.info(info)

    def error(self, error):
        self.logger.error(error)
