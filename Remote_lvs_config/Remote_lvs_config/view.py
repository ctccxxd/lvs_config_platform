# -*- coding: utf-8 -*-
from django.shortcuts import render
from lvs1.models import *
from lvs1.remoteupload import *
from lvs1.sql_update import *
from django.http import HttpResponse
import os
import sys
import re
import time
import paramiko
import socket 
import fcntl
import struct
#pattern={'Round-robin':'rr','WeightedRound-Robin':'wrr','Source-hash':'sh','Least-connect':'lc'}
'''cope with exception'''
def notice(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except BaseException as e:
            return HttpResponse('%s'%e)
    return wrapper

'''To check whether the input lvsNum is valid '''
def checklvsNUM(lvs):
     p = re.compile('^lvs\d+$')  
     if p.match(lvs):
         return True
     else:
         return False

"""split the arg3(string consists of ip and the signal * ) to IP list"""
def testpara_split(arg3): 
    count=0
    RIP=[]
    para2=arg3
    for i in str(para2):
        if i=='*':
            count=count+1
    for i in range(count+1):
        RIP.append(str(para2.split('*')[i]))
    return RIP
"""
Returns true if the given string is a well-formed IP address. 
Supports IPv4 and IPv6. 
"""
def checkIP(ip):  
    if not ip or '\x00' in ip:  
        # getaddrinfo resolves empty strings to localhost, and truncates  
        # on zero bytes.  
        return False  
    try:  
        res = socket.getaddrinfo(ip, 0, socket.AF_UNSPEC,  
                                 socket.SOCK_STREAM,  
                                 0, socket.AI_NUMERICHOST)  
        return bool(res)  
    except socket.gaierror as e:  
        if e.args[0] == socket.EAI_NONAME:  
            return False  
        raise  
    return True 
 
def check_VIP_information(ip_port):      
     p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?:(\d+))$')  
     if p.match(ip_port) and checkIP(ip_port.split(':')[0]):
         return True
     else:
         return False


"""
Returns the ip address of eth0 
"""
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def index(request):                                                      # To decorate the index html page 
    item= lvsinfo.objects.all()
    realservers=rsinfo.objects.all().order_by('-realserver_pool')
    lvs_list=get_lvs_num()
    return render(request, 'idz/demo.html',{'item':item,'realservers':realservers,'lvs_list':lvs_list})

@notice
def addlvs(request):                                                             #add lvs instance 
    arg2=request.GET['VIP']                                     
    arg3=request.GET['realserver']
    arg=[request.GET['lvsnum'],request.GET['targetIP'],arg2,arg3]
    """ some query results"""                                
    item_all=lvsinfo.objects.all().order_by('-lvsnum','VIP','realserver')
    lvs_vip=lvsinfo.objects.filter(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2])
    item_current=lvsinfo.objects.filter(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2],realserver=arg[3])
    TargetIP_current=lvsinfo.objects.filter(targetIP=arg[1])
    lvs_current=lvsinfo.objects.filter(lvsnum=arg[0])
    
    #To check whether the input is empty
    if arg[0]=='' or arg[1]=='' or arg[2]=='' or arg[3]=='Select one...': 
        return  HttpResponse('Please enter the whole information for adding!')

     
    if not checklvsNUM(arg[0]):
        return  HttpResponse('Please input valid LvsNum!')
    if not checkIP(arg[1]):
        return  HttpResponse('Please input valid target IP!')
    if not check_VIP_information(arg[2]):
        return HttpResponse('Please input valid VIP information (including port)!')
    if not checkIP(arg[3].split(':')[0]):
        return  HttpResponse('Please input valid realserver IP!')

    lvs_tarIP_get=lvsinfo.objects.filter(lvsnum=arg[0]).values('targetIP').distinct()
  #  return  HttpResponse('hha!%s'%lvs_tarIP_get[0]['targetIP'])
    if  str(lvs_current)!='[]':
        if  lvs_tarIP_get[0]['targetIP']!=arg[1]:
            return  HttpResponse('The '+arg[0]+'\'s '+'corresponding Target IP should be '+lvs_tarIP_get[0]['targetIP']+' !')
    else:
        if  str(TargetIP_current)!='[]' :
                return  HttpResponse('The target IP '+arg[1]+' has been configed!')

    # To check whether the lvsNum is in database
    if  str(item_current)!='[]' :       
        return  HttpResponse('The '+" realserver"+" has been added to this VIP!")
    if str(lvs_vip)!='[]':
        logo=1
    else:
        logo=0
      
    # To config the lvs 
    vip_port=arg2.split(':')[1]
    rs_port=arg3.split(':')[1]
    if lvs_config(arg[1],arg[2].split(':')[0],arg[3].split(':')[0],logo,vip_port,rs_port)==True:
        res=lvsinfo.objects.get_or_create(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2],realserver=request.GET['realserver'])
        js_update()
        js_update()
        return render(request, 'return1.html',{'item':item_all,'local_ip':get_ip_address('eth0')})
    else:
        return lvs_config(arg[1],arg[2].split(':')[0],arg[3].split(':')[0],logo,vip_port,rs_port)
         
 
def deletelvs(request):                                                     #del lvs instance                             
    vip_port=request.GET['cho_VIP'].split(':')[1]
    if ':' in request.GET['cho_realserver']:
        rs_port=request.GET['cho_realserver'].split(':')[1]
    arg=[request.GET['cho_lvsnum'],request.GET['cho_targetIP'],request.GET['cho_VIP'],request.GET['cho_realserver']] 
    """ some query results"""
    item_all=lvsinfo.objects.all().order_by('-lvsnum','VIP','realserver')
    lvs_lvs=lvsinfo.objects.filter(lvsnum=arg[0])
    item_vip=lvsinfo.objects.filter(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2])
    lvs_realserver=lvsinfo.objects.filter(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2],realserver=arg[3])
    if arg[0]=='Select one...' or arg[1]=='Select one...' or arg[2]=='Select one...' or arg[3]=='Select one...':
        if str(item_all)=='[]':  
            return HttpResponse('There is no any item in database!') 
        else:
            return  HttpResponse('Please enter your object for deleting!')
    if str(item_vip)=='[]':  
        return HttpResponse('There is no this VIP on server '+arg[0]+'!') 
    # To check whether the realserver is in database 
    if str(lvs_realserver)=='[]' and arg[3]!='All-RS':  
        return HttpResponse('There is no this realserver bound to '+arg[2]+'!')
 
    #To delete the lvs configuration
    if arg[3]!='All-RS':
        t=lvs_del_single_rs(arg[1],arg[2].split(':')[0],arg[3].split(':')[0],vip_port,rs_port)
        if  t==True or -1:
            lvsinfo.objects.filter(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2],realserver=arg[3]).delete()
            item_vip_after=lvsinfo.objects.filter(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2])
            if str(item_vip_after)=='[]': 
                if  lvs_del_whole_vip(arg[1],arg[2].split(':')[0],vip_port)==True:
                    pass
                else:
                    return lvs_del_whole_vip(arg[1],arg[2].split(':')[0],vip_port) 
            js_update()
            if  t==-1:
                information='The realserver is down, and please check it!\n\nThe system is deleting it from virtual server'+' '+arg[2]+'\n...'
                return render(request, 'not_working.html',{'information':information,'local_ip':get_ip_address('eth0')})
            return render(request, 'return1.html',{'item':item_all,'local_ip':get_ip_address('eth0')})
        else:
            return lvs_del_single_rs(arg[1],arg[2].split(':')[0],arg[3].split(':')[0],vip_port,rs_port)
    else:
        if  lvs_del_whole_vip(arg[1],arg[2].split(':')[0],vip_port)==True:
            lvsinfo.objects.filter(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2]).delete()
            js_update()
            return render(request, 'return1.html',{'item':item_all,'local_ip':get_ip_address('eth0')})
        else:
            return lvs_del_whole_vip(arg[1],arg[2].split(':')[0],vip_port) 
    

def findlvs(request):                                                           #find lvs instance
    arg=request.GET['lvsnum'] 
    lvs_current=lvsinfo.objects.filter(lvsnum=arg)
    item_all=lvsinfo.objects.all().order_by('-lvsnum','VIP','realserver')
    if str(item_all)=='[]': 
        return HttpResponse('There is no any item in database!') 
    if arg=='Select one...': 
            return  HttpResponse('Please enter your object for finding!')
    if arg=='all':
        return render(request, 'return.html',{'item':item_all})
    if str(lvs_current)=='[]':      # To check whether the lvsNum is in database
        return  HttpResponse('There is no '+arg+" in database!")
    else:
        return render(request, 'return.html',{'item':lvs_current})
@notice
def chglvs(request):                                                            #change lvs information
    arg3 = request.REQUEST.getlist('realserver') 
    arg3='*'.join(arg3)
    arg3_split=testpara_split(arg3)
    """ some query results"""
    arg=[request.GET['lvsnum'],request.GET['targetIP'],request.GET['VIP'],arg3] 
    item_all=lvsinfo.objects.all().order_by('-lvsnum','VIP','realserver')
    lvs_lvs=lvsinfo.objects.filter(lvsnum=arg[0])
    item_vip=lvsinfo.objects.filter(lvsnum=arg[0],VIP=arg[2])

    if arg[0]=='Select one...' or arg[1]=='Select one...' or arg[2]=='Select one...' or arg[3]=='':
        if str(item_all)=='[]':  
            return HttpResponse('There is no this item in database!') 
        else:
            return  HttpResponse('Please enter the whole information for changing!')
    if not checklvsNUM(arg[0]):
        return  HttpResponse('Please input valid lvsnum!')
    if not checkIP(arg[1]):
        return  HttpResponse('Please input valid target IP!')
    if not check_VIP_information(arg[2]):
        return HttpResponse('Please input valid VIP information (including port)!')
    
 
    vip_port=arg[2].split(':')[1]
    if str(item_vip)=='[]':  
        return HttpResponse('There is no this VIP on server '+arg[0]+'!')  
    lvs_tarIP_get=lvsinfo.objects.filter(lvsnum=arg[0]).values('targetIP').distinct()
    if  lvs_tarIP_get[0]['targetIP']!=arg[1]:
           return  HttpResponse('The '+arg[0]+'\'s '+'corresponding Target IP should be '+lvs_tarIP_get[0]['targetIP']+' !')
     #     To change the lvs configuration
    if lvs_chg(arg[1],arg[2].split(':')[0],arg[3],vip_port)==True:
        lvsinfo.objects.filter(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2]).delete()
        for i in arg3_split:
            lvsinfo.objects.get_or_create(lvsnum=arg[0],targetIP=arg[1],VIP=arg[2],realserver=i)
        js_update()
        return render(request, 'return1.html',{'item':item_all,'local_ip':get_ip_address('eth0')})
    else:
        return lvs_chg(arg[1],arg[2].split(':')[0],arg[3],vip_port)


    
            
