
###################################################################
#######  UDP listener program for Cluster Monitoring System  ######
###################################################################

import socket
import os


file1="./cluster_monitor_data_10sec.csv"

data_dic={}


UDP_PORT = 50065
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', UDP_PORT))



## Write the content of dictionary data into .csv file
def file_output(d, filename):
   if os.path.exists(file1):
      os.remove(file1)
   with open(filename, "a") as out_file:
         for k,v in d.items():
            line = '{}'.format(v)
            out_file.write(line+'\n')
           


try:
  
   while True:
     data, addr = sock.recvfrom(1024) 
     print "received message:", data
     y = data.strip().split(",")
     nodename=y[0]
     data_dic[nodename]=data
     print "the following is the content of data_dic"
     print data_dic.values()
     file_output(data_dic,file1)
      

finally:
   sock.close()



  


