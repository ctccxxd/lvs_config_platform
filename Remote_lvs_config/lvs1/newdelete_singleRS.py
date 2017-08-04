#!/usr/bin/env python   
# -*- coding: utf-8 -*-  
import os
import time
import math 
import sys
VIP=[]
VIP.append(sys.argv[1])
RIP=[]
RIP.append(sys.argv[2])
port_virtualserver=sys.argv[3]
port_realserver=sys.argv[4]
keepalived_configfile_path = '//etc//keepalived'+ os.sep+'keepalived.conf'

def lvs_delete(port_virtualserver):
    for i in VIP:
        for j in RIP:
            os.system('ipvsadm -d -t '+ str(i)+':'+str(port_virtualserver)+' -r '+str(j)) #delete lvs服务
# ipvsadm -D -t 10.9.9.9:80
#ipvsadm -d -t 10.3.103.10:80 -r 10.0.0.15

def delete_single_RS(VIP,RS):
    with open(keepalived_configfile_path,'r') as f:
        lines=f.readlines()
    with open(keepalived_configfile_path,'w') as f: 
        k=[]
        logo=0
        count=0
        logo1=0
        for i in lines:
            if logo==0 and 'virtual_server '+VIP+' '+port_virtualserver in i: 
                logo=1
            if logo==1 and 'real_server '+RS+' '+port_realserver in i:
                logo1=1
                continue
            if logo1==1 and '}' in i:
                count+=1
                if count==2:
                    logo1=0
                    logo=0
                    continue
            if logo1==1:
                continue
            f.write(i)  



lvs_delete(port_virtualserver)       #  delete lvs服务
delete_single_RS(VIP[0],RIP[0])
os.system('pkill -9 keepalived')
os.system('keepalived')
