#!/usr/bin/python

# Script will get the database name, put results into text file. 
# Dump of the database listed in the text will be executed 
# This script is MySQLdb wrapper - https://mysqlclient.readthedocs.io/user_guide.html, it is an interface to MySQLdatabase server using API


# Import python libraries
import MySQLdb as mysqldb
import os
import time
import datetime
import pipes

HOST = 'localhost'
USER = 'username'
CODE = 'code'
SOCKET ='/mysql/<db_name>/data/<db_name>.sock'
DBLIST = '/mysql/admin/scripts/dblist.txt'
DB_NAME = 'test'
BKUPLOC = '/mysql/backup/dump/'
TIMESTAMP = time.strftime('%Y%b%d-%H%M%S')
BKUDIR = BKUPLOC + TIMESTAMP

connect = MySQLdb.connect(host = HOST, user = USER, passwd = CODE, unix_socket = SOCKET)
cursor = connect.cursor()
cursor.execute("select schema_name from information_schema.schemata where schema_name not in ('mysql','information_schema','performance_schema','sys')")
data = cursor.fetchall()
with open('/mysql/admin/scripts/dblist.txt', 'w') as f:
    for row in data:
        print row [0]
        f.write("%s\n" % str(row [0]))
cursor.close()
connect.close()
sys.exit()

# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(BACKUPLOC)
except:
    os.mkdir(BACKUPLOC)

# Code for checking if you want to take single database backup or assigned multiple backups in DB_NAME.
print "checking for databases names file."
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print "Databases file found..."
    print "Starting backup of all dbs listed in file " + DB_NAME
else:
    print "Databases file not found..."
    print "Starting backup of database " + DB_NAME
    multi = 0

# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")

   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       #dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " -S" + SOCKET +" " + db + " > " + pipes.quote(BACKUPLOC) + "/" + db + ".sql"
       os.system(dumpcmd)
       compcmd = "tar -zcvf " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".tar.gz " +  pipes.quote(BACKUPLOC) + "/" + db + ".sql"
       os.system(compcmd)
       delcmd = "rm " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(delcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(BACKUPLOC) + "/" + db + ".sql"
   os.system(dumpcmd)
   compcmd = "tar -zcvf " + pipes.quote(BACKUPLOC) + "/" + db + ".tar.gz " +  pipes.quote(BACKUPLOC) + "/" + db + ".sql"
   os.system(compcmd)
   delcmd = "rm " + pipes.quote(BACKUPLOC) + "/" + db + ".sql"
   os.system(delcmd)

print "Backup script completed"
print "Your backups has been created in '" + BACKUPLOC + "' directory"
