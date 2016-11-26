#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Passenger(models.Model):
    passenger_name = models.CharField('乘车人姓名',max_length=20)
    passenger_id = models.CharField('身份证号码',max_length=20,primary_key=True)
    student = models.IntegerField('学生票',default=0)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.passenger_id

    def __unicode__(self):
    	return self.passenger_id



