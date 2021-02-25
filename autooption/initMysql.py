#!/usr/bin/env python

from Mysql import connect

message = connect()
cnn = message[0]
cursor = message[1]

query = 'drop table checkshow'
cursor.execute(query)

query = 'drop table recheck'
cursor.execute(query)

query = 'create table checkshow(id int not null primary key auto_increment, name char(40),status char(40))'
cursor.execute(query)

query = 'create table recheck(id int not null primary key auto_increment, name  char(50),string text(2048))'
cursor.execute(query)
cnn.commit()
cursor.close()
cnn.close()
