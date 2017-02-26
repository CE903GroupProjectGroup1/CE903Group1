import sys, socket, select, time
from math import *


import socket
import logging
import shutil
import os


file1="./cluster_monitor_data_10sec.csv"
#file2="./cluster_monitor_data.csv"
#file2_old="./cluster_monitor_data_old.csv"
#file_tmp="./cluster_monitor_data_tmp.csv"


logger = logging.getLogger(file1)
#hdlr = logging.FileHandler('./cluster_monitor_data_10sec.csv')
hdlr = logging.FileHandler(file1)
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter('%(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)



UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind(('', UDP_PORT))

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  print "received message:", data
  logger.info(data) 


