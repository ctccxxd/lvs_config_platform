#!/usr/bin/env python   
# -*- coding: utf-8 -*-  
import os
import time
import math 
import sys
from random import choice
VIP=[]
VIP.append(sys.argv[1]) 
RIP=[]
RIP_port_hash=[]
count=0
para2=sys.argv[2]
port_virtualserver=sys.argv[3]
#port_realserver=sys.argv[4]
keepalived_configfile_path = '//etc//keepalived'+ os.sep+'keepalived.conf'
for i in str(para2):
    if i=='*':
        count=count+1
for i in range(count+1):
    RIP.append(str(para2.split('*')[i].split(':')[0]))
    RIP_port_hash.append((str(para2.split('*')[i].split(':')[0]),str(para2.split('*')[i].split(':')[1])))

def lvs_delete(port_virtualserver):
    for i in VIP:
        os.system('ipvsadm -D -t '+str(i)+':'+str(port_virtualserver)) #deletelvs服务
# ipvsadm -D -t 10.9.9.9:80

'''配置lvs函数'''

def lvs_config(port_realserver,port_virtualserver):
    for i in VIP:
        os.system('ipvsadm -A -t '+ str(i)+':'+str(port_virtualserver)+' -s '+'rr') #起一个lvs服务
        for j in RIP:
            os.system('ipvsadm -a -t '+str(i)+':'+str(port_virtualserver)+' -r '+str(j)+':'+str(port_realserver)+' -m')
    os.system('echo 1 >/proc/sys/net/ipv4/ip_forward') #开启ipv4转发


def simple_addRS(RS):
    with open(keepalived_configfile_path,'a') as f:
        for i in RS:
            f.write('\treal_server '+i[0]+' '+i[1]+' {\n\tweight 1\n\tTCP_CHECK {\n\t\tconnect_timeout 3\n\t\tnb_get_retry 3\n\t\tdelay_before_retry 3\n\t\tconnet_port '+i[1]+'\n\t}'+'\n\t\t}\n')
        f.write('}\n')

def add_virtualserver(VIP,RS,port_virtualserver):
    with open(keepalived_configfile_path,'r') as f:
        lines=f.readlines()
    with open(keepalived_configfile_path,'w') as f: 
        for i in lines:
            if 'virtual_server_group' in i:
               f.write(i+'\t'+VIP+' '+str(port_virtualserver)+'\n')
               continue
            f.write(i)
        f.write('virtual_server '+VIP+' '+str(port_virtualserver)+'{\n\tdelay_loop 6\n\tlb_algo rr\n\tlb_kind FNAT\n\tprotocol TCP\n\tladdr_group_name laddr_g1\n\tquorum 1\n\thysteresis 0\n\tquorum_up \"ip addr  add '+VIP+'/32 dev lo;ip addr  add 127.0.0.1/8 dev lo;\"\n\tquorum_down \"ip addr  del '+VIP+'/32 dev lo;\"\n\n')
    simple_addRS(RS)

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
            if logo1==1 and 'virtual_server' in i:
                logo1=0
            if logo1==1:
                continue
            f.write(i)   

def chg(VIP,RS,port_virtualserver):
    delete_whole(VIP)
    add_virtualserver(VIP,RS,port_virtualserver)


lvs_delete(port_virtualserver)             #配置lvs
#lvs_config(port_realserver,port_virtualserver)                     
chg(VIP[0],RIP_port_hash,port_virtualserver)
os.system('pkill -9 keepalived')
while True:
    if len(os.popen('netstat -anp|grep keepalived').readlines())==0:
        os.system('keepalived')
        break
    else:
        os.system('pkill -9 keepalived')
        time.sleep(2)
os.system('echo 1 >/proc/sys/net/ipv4/ip_forward')

while True:
    if len(os.popen('netstat -anp|grep keepalived').readlines())>0:
        break
    else:
        os.system('keepalived')
        time.sleep(1)
#VIP.append(str(sys.argv[2]))
