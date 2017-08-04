#!/usr/bin/env python   
# -*- coding: utf-8 -*-  
import os
import time
import math 
import sys
from random import choice
  
targetIP=sys.argv[1]  
VIP=[]  
VIP.append(str(sys.argv[2]))
RIP=['10.0.0.1','10.0.0.2']
#VIP=['10.3.103.7']
DIP='10.0.0.1'
eth_list={'eth0':'dhcp','eth1':'static'}
ethlist=['eth0','eth1']
address=['10.3.103.7','10.0.0.1']
Gateway=['10.3.103.254','']
netmask=['255.255.255.0','255.255.255.0']


'''配置lvs函数'''
def lvs_config():
    for i in VIP:
        os.system('ipvsadm -A -t '+ str(i)+':80 '+'-s '+'rr') #起一个lvs服务
        for j in RIP:
            os.system('ipvsadm -a -t '+str(i)+':80 '+'-r'+str(j)+':80 '+'-m')
    os.system('echo 1 >/proc/sys/net/ipv4/ip_forward') #开启ipv4转发


'''配置写入函数'''
#静态ip配置函数
def static_config(index,eth):
    f = open("/etc/network/interfaces", "a+")
    if Gateway[index]=='':
        f.write('\n'+'auto '+eth+'\n'+'iface '+eth+' inet static'+'\n'+'address '+address[index]+'\n'+'netmask '+netmask[index])
    else:     
        f.write('\n'+'auto '+eth+'\n'+'iface '+eth+' inet static'+'\n'+'address '+address[index]+'\n'+'netmask '+netmask[index]+'\n'+'gateway '+Gateway[index])
    f.close()
#动态ip配置函数
def dhcp_config(index,eth):
    f = open("/etc/network/interfaces", "a+")
    f.write('\n'+'auto '+eth+'\n'+'iface '+eth+' dhcp')
    f.close()
#网卡配置函数入口
def add_config(eth):
    if eth_list[eth]=='static':        #将配置分为静态ip和动态ip
        static_config(ethlist.index(eth),eth)
    if eth_list[eth]=='dhcp':
        dhcp_config(ethlist.index(eth),eth)
	
'''相应网卡配置流程'''
os.system('ipvsadm -C')# -t '+ VIP[0]+':80 ') 
lvs_config()                      #配置lvs
os.system('rm -r /etc/network/interfaces')    #将原来的nterfaces文件删除
f = open("/etc/network/interfaces", "a+")
f.write('auto lo'+'\n'+'iface lo inet loopback') #写入本地配置
f.close()
for eth in ethlist:  
    print(ethlist.index(eth),eth)                           #配置其他全部网卡
    add_config(eth)
os.system('service network-manager restart') #重启网络 
time.sleep(3)
logo=0
ping=['ping -c 5 baidu.com','ping -c 5 sohu.com']
while True:               #不断重启网络直到ping 通百度或者搜狐服务器
    for i in os.popen(choice(ping)).readlines():
        if  'time=' in i:
            logo=1
            print "It has been ok and %s"%i 
            _LINKFINISHEDLOGO_ 
            break
            break
    if logo==0:
        os.system('service network-manager restart')
        time.sleep(3)

