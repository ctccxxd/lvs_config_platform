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
RIP.append(sys.argv[2])
logo=sys.argv[3]
keepalived_configfile_path = '//etc//keepalived'+ os.sep+'keepalived.conf'
port_virtualserver=sys.argv[4]
port_realserver=sys.argv[5]

'''配置lvs函数'''
def lvs_config(port_realserver,port_virtualserver):
    if logo=='0':
        for i in VIP:
            os.system('ipvsadm -A -t '+ str(i)+':'+str(port_virtualserver)+' -s '+'rr') #起一个lvs服务
            for j in RIP:
                os.system('ipvsadm -a -t '+str(i)+':'+str(port_virtualserver)+' -r '+str(j)+':'+str(port_realserver)+' -m')
        os.system('echo 1 >/proc/sys/net/ipv4/ip_forward') #开启ipv4转发
    else:
        for i in VIP:
            for j in RIP:
                os.system('ipvsadm -a -t '+str(i)+':'+str(port_virtualserver)+' -r '+str(j)+':'+str(port_realserver)+' -m')

def simple_addRS(RS,port_realserver):
    with open(keepalived_configfile_path,'a') as f:
        for i in RS:
            f.write('\treal_server '+i+' '+str(port_realserver)+' {\n\tweight 1\n\tTCP_CHECK {\n\t\tconnect_timeout 3\n\t\tnb_get_retry 3\n\t\tdelay_before_retry 3\n\t\tconnet_port '+str(port_realserver)+'\n\t}'+'\n\t\t}\n')
        f.write('}\n')

def add_virtualserver(VIP,RS,port_realserver,port_virtualserver):
    with open(keepalived_configfile_path,'r') as f:
        lines=f.readlines()
    with open(keepalived_configfile_path,'w') as f: 
        for i in lines:
            if 'virtual_server_group' in i:
               f.write(i+'\t'+VIP+' '+str(port_virtualserver)+'\n')
               continue
            f.write(i)
        f.write('virtual_server '+VIP+' '+str(port_virtualserver)+'{\n\tdelay_loop 6\n\tlb_algo rr\n\tlb_kind FNAT\n\tprotocol TCP\n\tladdr_group_name laddr_g1\n\tquorum 1\n\thysteresis 0\n\tquorum_up \"ip addr  add '+VIP+'/32 dev lo;ip addr  add 127.0.0.1/8 dev lo;\"\n\tquorum_down \"ip addr  del '+VIP+'/32 dev lo;\"\n\n')
    simple_addRS(RS,port_realserver)

def add_RS_single(VIP,RS,port_realserver,port_virtualserver):
    with open(keepalived_configfile_path,'r') as f: 
        logo=0
        VIP_exist=0
        content = f.read()
        post = content.find('virtual_server '+VIP+' '+port_virtualserver)
        if post != -1:
            VIP_exist=1
    with open(keepalived_configfile_path,'r') as f:
        lines=f.readlines()
    if VIP_exist==1:
        with open(keepalived_configfile_path,'w') as f:
            for i in lines:
                if (logo==0 and 'virtual_server '+VIP+' '+port_virtualserver in i) and '#' not in i: 
                    logo=1
                if logo==1 and 'real_server' in i:
                    logo=0
                    RS=RS[0]
                    f.write('\treal_server '+RS+' '+str(port_realserver)+' {\n\tweight 1\n\tTCP_CHECK {\n\t\tconnect_timeout 3\n\t\tnb_get_retry 3\n\t\tdelay_before_retry 3\n\t\tconnet_port '+str(port_realserver)+'\n\t}'+'\n\t\t}\n'+i)
                    continue
                f.write(i)
    else:
        add_virtualserver(VIP,RS,port_realserver,port_virtualserver)



#lvs_config(port_realserver,port_virtualserver)                      #配置lvs
add_RS_single(VIP[0],RIP,port_realserver,port_virtualserver)
os.system('pkill -9 keepalived')
os.system('keepalived')
os.system('echo 1 >/proc/sys/net/ipv4/ip_forward')
#VIP.append(str(sys.argv[2]))
