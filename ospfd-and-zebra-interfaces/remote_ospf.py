# -*- coding: utf-8 -*-
import paramiko
import os
import sys
import time
serverUser = 'root'
serverPwd = 'PYTym9bh'
para=sys.argv[1:]

arg={}
for i in para:
   if i.split(':')[0] not in arg.keys():
       s=i.split(':')[1]
       arg.setdefault(i.split(':')[0],s)


serverIp=arg['tip']
arg.pop('tip')

def notice(func):
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except paramiko.AuthenticationException as e:
            print 'Please check the '+args[0]+'\'s'+ ' password! %s'%e
        except paramiko.SSHException as e:
            print 'Please check the ssh! %s'%e
        except BaseException as e:
            print 'Problem: %s'%e
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
    localpath = r'//home//dengyl//ENV//lvs_config_platform//ospfd-and-zebra-interfaces' + os.sep + localFile
    remotepath = '//home' + os.sep+localFile
    t = paramiko.Transport(( serverIp ,22))
    t.connect(username = serverUser , password = serverPwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(localpath,remotepath)
    t.close()
    



def exeModuleFile(serverIp):
    sshd = ssh_connect( serverIp , serverUser , serverPwd )
    cmd=ssh_exec_cmd(sshd,'python //home//ospfd.py %s'%str(arg))[2]
    t=cmd.readlines()
    if len(t)>0:
        raise BaseException("%s"%t)
    ssh_close( sshd )



@notice
def remote_ospfd(serverIp):
    ftpModuleFile(serverIp,'ospfd.py')
    exeModuleFile(serverIp)
    print 'Ospfd configuration on'+' '+'%s has been successful!'%serverIp
    print '              ***Ospfd restart!***'
remote_ospfd(serverIp)



