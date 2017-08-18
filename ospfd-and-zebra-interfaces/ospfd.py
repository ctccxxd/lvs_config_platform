#!/usr/bin/env python   
# -*- coding: utf-8 -*-  
import os
import time
import math 
import sys
para=''
for i in range(len(sys.argv)):
    if i==0:
        continue
    para+=str(sys.argv[i])
arg={}
para= para[1:-1].split(',')
for i in para:
   arg.setdefault(i.split(':')[0],i.split(':')[1])
area='0.0.0.0'

ospfd_configfile_path = '//etc//quagga'+ os.sep+'ospfd.conf'

def format(arg):
   s=''
   for i in arg.keys():
       s=s+'\n'+' '+'network'+' '+i+'/'+str(arg[i])+' '+'area '+area
   return s

str=format(arg)
with open(ospfd_configfile_path,'r') as file:
    content = file.read()
    post = content.find('router ospf')
    if post != -1:
        content = content[:post+len('router ospf')]+str
        with open(ospfd_configfile_path,'w') as file:
            file.write(content+'\n'+'!'+'\n'+'line vty'+'\n'+'!')
    file.close()
os.system('pkill -9 ospfd')
os.system('ospfd -d ')

