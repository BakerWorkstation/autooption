#!/usr/bin/env python

import yaml

import mysql.connector

def connect():
    try:
        filedir = 'autooption/item/'
        zabbixconf = '%szabbix.yaml' % filedir
        stream = file(zabbixconf, 'r')
    except IOError:
        filedir = 'item/'
        zabbixconf = '%szabbix.yaml' % filedir
        stream = file(zabbixconf, 'r')

    config = yaml.load(stream)
    try:
        cnn = mysql.connector.connect(**config)
        cursor = cnn.cursor()
        return (cnn, cursor)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
        return None

