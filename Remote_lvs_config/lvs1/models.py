# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class lvsinfo(models.Model):
    lvsnum = models.CharField(db_column='primaryStorageTotal',max_length=20)
    targetIP = models.CharField(max_length=20)
    VIP = models.CharField(max_length=20)
    realserver=models.CharField(max_length=20,blank=True)

class rsinfo(models.Model):
    realserver_pool=models.CharField(max_length=20)

    
