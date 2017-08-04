#!/usr/bin/env python   
# -*- coding: utf-8 -*-  
import os
import time
import math 
import sys
from random import choice
port_virtualserver=sys.argv[2]
VIP=[]
VIP.append(sys.argv[1])
keepalived_configfile_path = '//etc//keepalived'+ os.sep+'keepalived.conf'
def lvs_delete(port_virtualserver):
    for i in VIP:
        os.system('ipvsadm -D -t '+ str(i)+':'+str(port_virtualserver)) #delete lvs服务
# ipvsadm -D -t 10.9.9.9:80

def delete_whole(VIP):
    with open(keepalived_configfile_path,'r') as f:
        lines=f.readlines()
    with open(keepalived_configfile_path,'w') as f: 
        logo=0
        logo1=0
        for i in lines:
            if 'virtual_server_group' in i:
               logo=1
            if (VIP in i and 'virtual_server' not in i) and (logo==1 and '#' not in i) and (port_virtualserver in i):
                logo=0
                continue
            if logo1==0 and 'virtual_server '+VIP in i and port_virtualserver in i: 
                logo1=1
                continue
            if (logo1==1 and 'virtual_server' in i) and '#' not in i:
                logo1=0
            if logo1==1:
                continue
            f.write(i)   

lvs_delete(port_virtualserver)       #  delete lvs服务
delete_whole(VIP[0])
os.system('pkill -9 keepalived')
os.system('keepalived')
