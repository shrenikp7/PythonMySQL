#!/usr/bin/python

## Script Name : bkup.py
## Script Purpose: Execute full  backup of the MySQL Enterprise, compress it, check backup job status, email backup log, if backup fail send notification

# Import python libraries
import os
import time
import datetime
import pipes
import socket
import subprocess

host = socket.gethostname()
date = time.strftime('%Y%b%d-%H%M%S')
date1 = time.strftime('%Y-%m-%d.%H-%M-%S')
backupdir="--backup-dir=/tmp/backup" + date
backupimage="--backup-image=/mysql/<NFS>/"+host+".mts.backup.mbi_" + date
image="backup-to-image --compress"
logfile="/tmp/backup"+date+'/meta/MEB_'+date1+'.log'
mail_list="shrenik.parekh\@<domain>.com"
base_path = '/mysql/<NFS>'
print "Bakup start date and time: ", datetime.datetime.now()
#### Full backup execution
####
bkupcmd = "/bin/mysqlbackup" + " " + backupdir + " " + backupimage + " " + image
#### Execute backup command and check backup command status also
bkupresult=os.system(bkupcmd)
#### Check Bckup Status 
if bkupresult ==0:
 mailcmd = "mailx -s 'MEB Backup Log ' " +  mail_list + "< "+ logfile
 os.system(mailcmd)
else:
 mailcmd = "mailx -s 'MEB Backup FAILED ' " +  mail_list
 os.system(mailcmd)
print "Backup Complete date and time: ", datetime.datetime.now()
####
#### Folwoing funciton remove files older than 7 days
####
def remove_files(dir_path, n):
    all_files = os.listdir(dir_path)
    now = time.time()
    n_days = n * 86400
    for f in all_files:
        file_path = os.path.join(dir_path, f)
        if not os.path.isfile(file_path):
            continue
        if os.stat(file_path).st_mtime < now - n_days:
            os.remove(file_path)
            print("Deleted ", f)

remove_files(base_path, 7)

# End of script
