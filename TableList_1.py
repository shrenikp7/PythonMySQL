#!/usr/bin/python

####
#### Following script will read db name from txt file, Store db name in array, 
#### create file for each database, execute SQL statement to fetch table name, 
#### put output of sql statement in file and close the file. 
#### Scritp is running for loop inside the for loop.
####
import MySQLdb
import os
import time
import datetime
import sys

DBLIST = '/mysql/admin/scripts/dblist.txt'

HOST = 'localhost'
USER = '<id>'
CODE = 'code'
SOCKET = '/data/mysql/<db_name>.sock'

connect = MySQLdb.connect(host = HOST, user = USER, passwd = CODE, unix_socket = SOCKET)
cursor = connect.cursor()
in_file = open(DBLIST,"r")
with open(DBLIST) as f:
    content = f.readlines()
    f.close()
content = [x.strip() for x in content]

for db in content:
    print(db)
    f=open('/mysql/admin/scripts/dbfiledir/'+ db+'.txt', 'w')
    sql='select TABLE_NAME from information_schema.tables where TABLE_SCHEMA=' + "'" + db + "'" + ";"
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        f.write("%s\n" % str(row [0]))
    f.close()
cursor.close()
connect.close()
sys.exit()
