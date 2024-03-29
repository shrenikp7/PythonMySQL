####
#### Following script will read table name from the txt file, create file name with table name
#### execute SQL statement to list partitions exists for the table, save in file and close file
#### This script can read the file generated by script TableList.py which has table names.
####

#!/usr/bin/python
import MySQLdb
import os
import time
import datetime
import sys

TBLIST = '/mysql/admin/scripts/dbfiledir/<tab_name>.txt'

HOST = 'localhost'
USER = '<id>'
CODE = '<code>'
SOCKET = '/data/mysql/<db_name>.sock'

connect = MySQLdb.connect(host = HOST, user = USER, passwd = CODE, unix_socket = SOCKET)
cursor = connect.cursor()
in_file = open(TBLIST,"r")
with open(TBLIST) as f:
    content = f.readlines()
    f.close()
content = [x.strip() for x in content]

for tab in content:
    f=open('/mysql/admin/scripts/dbfiledir/tabfiledir/'+ tab +'.txt', 'w')
    sql='SELECT distinct(PARTITION_NAME), TABLE_NAME FROM INFORMATION_SCHEMA.PARTITIONS WHERE TABLE_NAME=' + "'" + tab + "'" + ";"
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        f.write("%s\n" % str(row [0]))
    f.close()
cursor.close()
connect.close()
sys.exit()
