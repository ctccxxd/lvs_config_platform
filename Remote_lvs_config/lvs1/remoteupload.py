# -*- coding: utf-8 -*-
import paramiko
import os
import sys
import time
#import traceback
from django.shortcuts import render
from models import *
from django.http import HttpResponse
from django.core import *
serverUser = 'root'
serverPwd = '11223'


def notice(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except paramiko.AuthenticationException as e:
            return HttpResponse('Please check the '+args[0]+'\'s'+ ' password! %s'%e)
        except paramiko.SSHException as e:
            return HttpResponse('Please check the ssh! %s'%e)
        except BaseException as e:
            return HttpResponse('Problem: %s'%e)
    return wrapper


def ssh_connect( _host, _username, _password ):
    _ssh_fd = paramiko.SSHClient()
    _ssh_fd.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    _ssh_fd.connect( _host, username = _username, password = _password )
    return _ssh_fd

def ssh_exec_cmd( _ssh_fd, _cmd ):
    return _ssh_fd.exec_command( _cmd )

def ssh_close( _ssh_fd ):
    _ssh_fd.close()


def ftpModuleFile(serverIp,localFile):
    localpath = r'//home//xiaodong//Desktop//Remote_lvs_config/lvs1' + os.sep + localFile
    remotepath = '//home' + os.sep+localFile
    t = paramiko.Transport(( serverIp ,22))
    t.connect(username = serverUser , password = serverPwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(localpath,remotepath)
    t.close()
    

def exeModuleFile(serverIp,VIP,realserver,logo,vip_port,rs_port):
    sshd = ssh_connect( serverIp , serverUser , serverPwd )
    cmd=ssh_exec_cmd(sshd,'python //home//new.py %s %s %s %s %s'%(VIP,realserver,logo,vip_port,rs_port))[2]
    t=cmd.readlines()
    if len(t)>0:
        raise BaseException("%s"%t)
    ssh_close( sshd )

def exeModuleFile_single_rs(serverIp,VIP,realserver,vip_port,rs_port):
    sshd = ssh_connect( serverIp , serverUser , serverPwd )
    cmd=ssh_exec_cmd(sshd,'python //home//newdelete_singleRS.py %s %s %s %s'%(VIP,realserver,vip_port,rs_port))[2]
    t=cmd.readlines()
    if len(t)>0:
        raise BaseException("%s"%t)
    ssh_close( sshd )

def exeModuleFile_whole_vip(serverIp,VIP,vip_port):
    sshd = ssh_connect( serverIp , serverUser , serverPwd )
    cmd=ssh_exec_cmd(sshd,'python //home//newdelete.py %s %s'%(VIP,vip_port))[2]
    t=cmd.readlines()
    if len(t)>0:
        raise BaseException("%s"%t)
    ssh_close( sshd )

def exeModuleFile_chg(serverIp,VIP,realserver,vip_port):
    sshd = ssh_connect( serverIp , serverUser , serverPwd )
    cmd=ssh_exec_cmd(sshd,'python //home//newchg.py %s %s %s'%(VIP,realserver,vip_port))[2]
    t=cmd.readlines()
    if len(t)>0:
        raise BaseException("%s"%t)
    ssh_close( sshd )


@notice
def lvs_del_whole_vip(serverIp,VIP,vip_port):
    ftpModuleFile(serverIp,'newdelete.py')
    exeModuleFile_whole_vip(serverIp,VIP,vip_port)
    return True



def lvs_del_single_rs(serverIp,VIP,realserver,vip_port,rs_port):
    try:
        ftpModuleFile(serverIp,'newdelete_singleRS.py')
        t=exeModuleFile_single_rs(serverIp,VIP,realserver,vip_port,rs_port)
        return True
    except paramiko.AuthenticationException as e:
        return HttpResponse('Please check the '+args[0]+'\'s'+ ' password! %s'%e)
    except paramiko.SSHException as e:
        return HttpResponse('Please check the ssh! %s'%e)
    except BaseException as e:
        if 'Memory allocation' in str(e):
            return -1
        else:
            return HttpResponse('Problem: %s'%e)


@notice
def lvs_chg(serverIp,VIP,realserver,vip_port):
    ftpModuleFile(serverIp,'newchg.py')
    exeModuleFile_chg(serverIp,VIP,realserver,vip_port)
    return True

@notice
def lvs_config(serverIp,VIP,realserver,logo,vip_port,rs_port):
    ftpModuleFile(serverIp,'new.py')
    exeModuleFile(serverIp,VIP,realserver,logo,vip_port,rs_port)
    return True





