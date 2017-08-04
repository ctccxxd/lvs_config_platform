#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import MySQLdb


def js_update():
   sql1 = "SELECT distinct primaryStorageTotal FROM lvs1_lvsinfo"
   sql2 = "SELECT distinct targetIP FROM lvs1_lvsinfo"
# 打开数据库连接
   db = MySQLdb.connect("localhost","root","","mysql" )
   dic={}
# 使用cursor()方法获取操作游标 
   cursor = db.cursor()
   try:
      lvsnum1=getlist(sql1,cursor) 

      IPtarget2=getlist(sql2,cursor)  
      f=range(len(lvsnum1))
      for i in f:
         dic.setdefault(lvsnum1[i],IPtarget2[i])
      lvsnum1=sorted(lvsnum1) 
     #begin write
      string='function Dsy(){'+'\n'+'   this.Items = {};'+'\n'+'};'+'\n'+'Dsy.prototype.add = function(id,iArray){'+'\n'+'   this.Items[id]=    iArray;'+'\n'+ '};'+'\n'+'Dsy.prototype.Exists = function(id){'+'\n'+'   if(typeof(this.Items[id]) == \"undefined\") return false;'+'\n'+'   return true;'+'\n'+'};'+'\n'+'var dsy = new Dsy();'
      with open("static/js/city4.city.js","w+") as file:
         file.write(string)     
      with open("static/js/city4.city.js","a+") as file:
         file.write('\n'+'dsy.add(\"0\",'+str(lvsnum1)+');')

      for i in f:
         with open("static/js/city4.city.js","a+") as file:
            file.write('\n'+'dsy.add(\"0_'+str(i)+"\","+"[\""+str(dic[lvsnum1[i]])+"\"]"+');')

   
      for j in f:
         sql3 = "SELECT distinct VIP FROM lvs1_lvsinfo WHERE targetIP='%s'" %dic[lvsnum1[j]]
         VIP3=getlist(sql3,cursor)
         with open("static/js/city4.city.js","a+") as file:
            file.write('\n'+'dsy.add(\"0_'+str(j)+"_"+"0\","+str(VIP3)+');')
         for k in range(len(VIP3)):
            sql4 = "SELECT distinct realserver FROM lvs1_lvsinfo WHERE targetIP='%s' AND VIP='%s'" %(dic[lvsnum1[j]],VIP3[k])
            realserver=getlist(sql4,cursor)
            realserver.insert(0,'All-RS')
            with open("static/js/city4.city.js","a+") as file:
               file.write('\n'+'dsy.add(\"0_'+str(j)+"_0_"+str(k)+"\","+str(realserver)+');')  
   except BaseException as e:
      print "Error: %s"%e
   db.close()

def get_lvs_num():
   sql = "SELECT distinct primaryStorageTotal FROM lvs1_lvsinfo"
   db = MySQLdb.connect("localhost","root","","mysql" )
   cursor = db.cursor()
   try:
      lvsnum1=getlist(sql,cursor)
      lvsnum1=sorted(lvsnum1) 
   except BaseException as e:
      print "Error: %s"%e
   return lvsnum1
   db.close()   


def getlist(sql,cursor):
   cursor.execute(sql)
   s = cursor.fetchall()
   h=[]
   for i in s:
      h.append(i[0])
   return h


