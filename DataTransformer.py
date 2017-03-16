import sys, socket, select, time
from math import *


import socket
import logging
import shutil
import os
import pandas as pd
from jsonify import convert


file1="./cluster_monitor_data_10sec.csv"
file2="./cluster_monitor_data.csv"
file2_old="./cluster_monitor_data_old.csv"
file_tmp="./cluster_monitor_data_tmp.csv"

### Read data 10sec file then update csv file
### Delete any old data in csv file if found for a node
### update_csv(file2_old, file_tmp)

## remove any empty lines in tmp file
def remove_empty_lines(filename):
   with open(filename) as in_file, open(filename, 'r+') as out_file:
        out_file.writelines(line for line in in_file if line.strip())
        out_file.truncate()


### for adding the title line 'Node,Time,CPU,Memory'
def line_prepender(filename):
    line="Node,Time,CPU,Memory"
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

### Check whether file contains nodename(pattern)        
def check(file,pattern):
    print "opening file :", file
    f2=open(file,"r")
    #datafile = file(f)
    found = False
    for line in f2:
        if pattern in line:
            found = True
            print " pattern found!", pattern
            break
    f2.close()
    return found


### Check if there is any missing Node entries in _tmp file.
### If so, copy the old data from _old.csv file.
  
def update_csv(f1,f2):

 f_1=open(f1,"r")
 #file2=open(f2,"r")
 result = open(f2, 'a')  # open file handle for write
 for line in f_1:
    new_line=line
    #print "checking : ", new_line
    y = new_line.strip().split(",")
    print y[0]
    pattern=y[0]
    
    if y[0]!="Node":
      found=check(f2,pattern)
      if found:
        print "Node entry exists"
        
      else:
        print "no data for the node : ", pattern, "Data will be added : ", new_line
        result.write(new_line)
 result.close()
 f_1.close()



while True:
  
 ## delete old 'data_tmp' file. 
 ## take a snapshot of 'data_10sec.csv' file and copy it as '_tmp' file for processing
 if os.path.exists(file_tmp):
    os.remove(file_tmp)
 shutil.copy2(file1, file_tmp)
 
 
 #rename cvs file to _old.csv
 if os.path.exists(file2_old):
    os.remove(file2_old)
 if os.path.exists(file2):
    os.rename(file2,file2_old)

 #Check whether there is any missing node entry in file_temp.
 #If so, copy the entry from _old.csv file.
 
 update_csv(file2_old, file_tmp)

 line_prepender(file_tmp)

 remove_empty_lines(file_tmp)


 
 df = pd.read_csv(file_tmp)
 df = df.sort(columns='Node')
 df.to_csv(file2, index=False)
 

 #Transform csv file to a Json file
 convert.jsonify(file2)
 

 #Interval changed from 10 sec to 1 sec as requested by customer
 time.sleep(1)
 #time.sleep(10)
 


