#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Train(models.Model):
    train_id = models.CharField('列车编号',max_length=5, primary_key=True)
    train_type = models.CharField('列车类型',max_length=1, default="K")
    num_station = models.IntegerField('总站点数',default=0)
    distance = models.FloatField('总里程数', default=0)

    def __str__(self):
        return self.train_id

    def __unicode__(self):
        return self.train_id

class Station(models.Model):
    station_id = models.IntegerField(default = 0, primary_key=True)
    station_name = models.CharField("途经车站", max_length=20)
    station_city = models.CharField("所属城市", max_length=20)

    def __str__(self):
        return self.station_name

    def __unicode__(self):
        return self.station_name


class Run(models.Model):
    @staticmethod
    def generateRunKey(station_id, train_id):
        run_key = '{:X<5}'.format(train_id) + '{:0>5}'.format(station_id)
        return run_key

    run_key = models.CharField(max_length=30, primary_key=True)
    station_name = models.ForeignKey(Station, on_delete=models.CASCADE)
    train_come_by = models.ForeignKey(Train, on_delete=models.CASCADE)
    order_of_station = models.IntegerField(default = 1)
    arrive_time = models.TimeField("到站时间", max_length = 10)
    distance_count = models.FloatField("里程数")
    count_over_night = models.IntegerField(default = -1)

    def __str__(self):
        return self.station_name

    def __unicode__(self):
        return self.run_key

    class Meta:
        ordering = ["train_come_by", "order_of_station"]

class Carriage(models.Model):
    @staticmethod
    def generateCarriageKey(train_id, carriage_id):
        carriage_key = '{:X<5}'.format(train_id) \
                   + '{:0>2}'.format(carriage_id)
        return carriage_key

    seat_type_list = (
        ('shangwu', '商务座'),
        ('yideng', '一等座'),
        ('erdeng', '二等座'),
        ('ruanwo', '软卧'),
        ('yingwo', '硬卧'),
        ('yingzuo', '硬座'),
    )
    carriage_key = models.CharField(max_length=30, primary_key = True)
    train_id = models.ForeignKey(Train, on_delete=models.CASCADE)
    carriage_id = models.IntegerField(default=1)
    num_seat = models.IntegerField(default=0)
    seat_type = models.CharField(max_length=10, choices = seat_type_list)

    def __str__(self):
        return self.carriage_key

    def __unicode__(self):
        return self.carriage_key


class TimeSpan(models.Model):
    time = models.DateField(primary_key=True)

class Seat(models.Model):
    @staticmethod
    def generateSeatRunKey(date, carriage_key, seat_id):
        seat_key = carriage_key \
                + date.time.strftime("%Y%m%d") \
                + '{:0>3}'.format(seat_id)
        return seat_key

    seat_key = models.CharField(max_length=30, primary_key=True)
    carriage = models.ForeignKey(Carriage, on_delete=models.CASCADE)
    seat_id = models.IntegerField()
    date = models.ForeignKey(TimeSpan)
    status = models.CharField(max_length=100)

    def __str__(self):
        return str(self.carriage.carriage_id) + str(self.date.time) \
               + str(self.seat_id)

    def __unicode__(self):
        return str(self.carriage.carriage_id) + str(self.date.time) \
               + str(self.seat_id)
    class Meta:
        ordering = ["seat_key", "date"]


class Price(models.Model):
    train_type = models.CharField('列车类型',max_length=20)
    seat_type = models.CharField('座位类型',max_length=20)
    ratio_student = models.FloatField('学生票打折系数',default=1)
    price_per_km = models.FloatField('每公里计价',default=0.5)

    def __str__(self):
        return self.train_type+" "+self.seat_type+" "+str(self.ratio_student)+" "+str(self.price_per_km)

    def __unicode__(self):
        return self.train_type+" "+self.seat_type+" "+str(self.ratio_student)+" "+str(self.price_per_km)

def loadPrice():
    p = Price.objects.create(train_type='G',seat_type=u'一等座',ratio_student=0.5,price_per_km=0.775)
    p.save()
    p = Price.objects.create(train_type='G',seat_type=u'二等座',ratio_student=0.5,price_per_km=0.446)
    p.save()
    p = Price.objects.create(train_type='G',seat_type=u'商务座',ratio_student=0.5,price_per_km=0.9)
    p.save()
    p = Price.objects.create(train_type='G',seat_type=u'硬座',ratio_student=0.5,price_per_km=0.3)
    p.save()
    p = Price.objects.create(train_type='G',seat_type=u'硬卧',ratio_student=0.5,price_per_km=0.7)
    p.save()
    p = Price.objects.create(train_type='G',seat_type=u'软卧',ratio_student=0.5,price_per_km=1.4)
    p.save()

    p = Price.objects.create(train_type='D',seat_type=u'一等座',ratio_student=0.5,price_per_km=0.348)
    p.save()
    p = Price.objects.create(train_type='D',seat_type=u'二等座',ratio_student=0.5,price_per_km=0.288)
    p.save()
    p = Price.objects.create(train_type='D',seat_type=u'商务座',ratio_student=0.5,price_per_km=0.5)
    p.save()
    p = Price.objects.create(train_type='G',seat_type=u'硬座',ratio_student=0.5,price_per_km=0.18)
    p.save()
    p = Price.objects.create(train_type='D',seat_type=u'硬卧',ratio_student=0.5,price_per_km=0.4)
    p.save()
    p = Price.objects.create(train_type='D',seat_type=u'软卧',ratio_student=0.5,price_per_km=1.2)
    p.save()

    p = Price.objects.create(train_type='K',seat_type=u'一等座',ratio_student=0.5,price_per_km=0.348)
    p.save()
    p = Price.objects.create(train_type='K',seat_type=u'二等座',ratio_student=0.5,price_per_km=0.288)
    p.save()
    p = Price.objects.create(train_type='K',seat_type=u'商务座',ratio_student=0.5,price_per_km=0.5)
    p.save()
    p = Price.objects.create(train_type='K',seat_type=u'硬座',ratio_student=0.5,price_per_km=0.16)
    p.save()
    p = Price.objects.create(train_type='K',seat_type=u'硬卧',ratio_student=0.5,price_per_km=0.853)
    p.save()
    p = Price.objects.create(train_type='K',seat_type=u'软卧',ratio_student=0.5,price_per_km=1.217)
    p.save()
