import sys, socket, select, time
from math import *


import socket
import logging
import shutil
import os


file1="./cluster_monitor_data_10sec.csv"

data_dic={}


UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))


def write_report(d, filename):
   if os.path.exists(file1):
      os.remove(file1)
   with open(filename, "a") as out_file:
         for k,v in d.items():
            line = '{}'.format(v)
            out_file.write(line+'\n')
           

try:
  
   while True:
     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
     print "received message:", data
     y = data.strip().split(",")
     nodename=y[0]
     data_dic[nodename]=data
     print "the following is the content of data_dic"
     print data_dic.values()
     write_report(data_dic,file1)
      

finally:
   sock.close()



  


