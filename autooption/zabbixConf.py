#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import yaml

host = '172.17.78.91'
user = 'zabbix'
password = 'zabbix'
port = '3306'
database = 'zabbix'

document = '''
host: %s
user: %s
password: %s
port: %s
database: %s
charset: utf8
''' %  (host, user, password, port, database)
stream = file('item/zabbix.yaml', 'w')
yaml.dump(yaml.load(document), stream)
