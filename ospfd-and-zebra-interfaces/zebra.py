#!/usr/bin/env python   
# -*- coding: utf-8 -*-  
import os
import time
import math 
import sys
import string

para=''
for i in range(len(sys.argv)):
    if i==0:
        continue
    para+=str(sys.argv[i])
arg={}
para= para[1:-2]
j=''
for i in para:
    if i=='[':
        continue
    j+=i
j=j.split('],')
os.system('echo '+str(j[1])+' >//home/para.txt')
arg={}
for i in j:
    for k in i.split(':')[1].split(','):
        if i.split(':')[0] not in arg.keys():
            arg.setdefault(i.split(':')[0],[str(k)])
        else:
            arg[i.split(':')[0]].append(str(k))

netmask_coreswitch=24

coreswitch_ip=arg['routerid']
coreswitch_ip.append(0)
arg_eth0=coreswitch_ip

zebra_configfile_path = '//etc//quagga'+ os.sep+'zebra.conf'

arg_eth1=[1]
arg_lo=arg['vip']
def format_eth(*arg):
   s='\n'+'!'+'\n'+'interface eth'+str(arg[-1])
   if len(arg)==1 and arg[0]==1:
       pass
   else:
       for i in range(len(arg)-1):
           s=s+'\n'+' '+'ip address '+arg[i]
   s+='\n'+' '+'ipv6 nd suppress-ra'
   return s

def format_lo(*arg):  
   s='\n'+'!'+'\n'+'interface lo'+' '
   for i in range(len(arg)):
       s=s+'\n'+' ip address '+arg[i]
   return s

str=format_eth(*arg_eth0)+format_eth(*arg_eth1)+format_lo(*arg_lo)


with open(zebra_configfile_path,'r') as file:
    content = file.read()
    post = content.find('debug zebra rib')
    if post != -1:
        content = content[:post+len('debug zebra rib')]+str
        with open(zebra_configfile_path,'w') as file:
            file.write(content+'\n'+'!'+'\n'+'router-id '+coreswitch_ip[0][0:-3]+'\n'+'ip forwarding'+'\n'+'!'+'\n'+'!'+'\n'+'line vty'+'\n'+'!')
    file.close()
os.system('pkill -9 zebra')
os.system('zebra -d ')

