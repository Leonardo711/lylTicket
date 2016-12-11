#-*-coding:utf-8-*-
from __future__ import unicode_literals

from django.db import models

from trainManage.models import Train,Station,Seat

# Create your models here.

class Order(models.Model):
    order_id = models.CharField('订单编号',max_length=20,primary_key=True)
    user_name = models.CharField('用户名',max_length=20)
    passenger_name = models.CharField('乘客姓名',max_length=20)
    passenger_id = models.CharField('乘客身份证号',max_length=20)
    passenger_phone = models.CharField('电话',max_length=10)
    student = models.IntegerField('学生票',default=0)
    order_time = models.DateTimeField('订票时间')
    train_name = models.ForeignKey(Train, on_delete=models.CASCADE)
    start_station = models.ForeignKey(Station,on_delete=models.CASCADE,related_name='start_station')
    end_station = models.ForeignKey(Station,on_delete=models.CASCADE,related_name='end_station')
    trip_date = models.DateTimeField('出发日期')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    pay = models.FloatField('金额',default = 0)
    order_status = models.IntegerField('订单状态',default=0) #0 train does not go;1 order is completed ; 2 order is canceled 

    def __str__(self):
        return self.order_id

    def __unicode__(self):
        return self.order_id
