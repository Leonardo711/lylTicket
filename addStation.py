# -*- coding: utf-8 -*-
import os
import sys
import django
#import ticket2016.settings
#from adduser.models import User, Passenger, User_Passenger, Price, Station
from trainManage.models import *
import train
import pinyin
'''
def addUser(user_name,password,email_address):
    usr = User(user_name=user_name,
                password=password,
                email_address=email_address)
    usr.save()

def addPassenger(passenger_name,passenger_id,student):
    psg = Passenger(passenger_name=passenger_name,
                passenger_id=passenger_id,
                student=student)
    psg.save()

def deleteUser(user_name):
    usr = User.objects.get(user_name=user_name)
    usr.delete()

def deletePassenger(passenger_id):
    psg = Passenger.objects.get(passenger_id=passenger_id)
    psg.delete()

def addUser_Passenger(user,passenger):
    u_p = User_Passenger(user,passenger)
    u_p.save()

def deleteUser_Passenger(user_name,passenger_id):
    u_p = User_Passenger.objects.get(user_name=user_name,passenger_id=passenger_id)
    u_p.delete()


def addPrice(train_type,seat_type,ratio_student,price_per_km):
    price = Price(train_type=train_type,
                seat_type=seat_type,
                ratio_student=ratio_student,
                price_per_km=price_per_km)
    price.save()
'''
def addStation(station_id,station_name,station_city):
    station = Station(station_id=station_id,
                    station_name=station_name,
                    station_city=station_city)
    station.save()

if __name__ == '__main__':
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticket2016.settings")
    #django.setup()
    cityset_num = range(10)
    cityset = [u'北京',u'上海',u'广州',u'深圳',u'天津',u'重庆',u'苏州',u'武汉',
               u'成都',u'杭州',u'南京',u'青岛',u'长沙']
    cityset_pinyin = ['beijing','shanghai','guangzhou','shenzhen',
                      'tianjin','chongqing','suzhou','wuhan',
                      'chengdu','hangzhou','nanjing','qingdao','changsha']
    num = 0
    for i in xrange(10):
        from_city = cityset[i]
        city_stations_set = set([])       
        for j in xrange(10):
            if i != j:
                to_city = cityset[j]
                
                #from_city_pinyin = pinyin.get(from_city,'','strip')
                #to_city_pinyin = pinyin.get(to_city,'','strip')
                #print from_city_pinyin+' to '+to_city_pinyin
                
                from_city_pinyin = cityset_pinyin[i]
                to_city_pinyin = cityset_pinyin[j]
                
                from_stations_set, to_stations_set = train.getStations(from_city_pinyin,to_city_pinyin)
                city_stations_set.update(from_stations_set)
        print from_city + u' 有下面几个车站:'
        for station in city_stations_set:
            print station
            num = num + 1
            addStation(str(num),station,from_city)
        print 
        
               
'''        
    from_city = u'天津'
    to_city = u'北京'
    from_city_pinyin = pinyin.get(from_city,'','strip')
    to_city_pinyin = pinyin.get(to_city,'','strip')
    print from_city_pinyin+' to '+to_city_pinyin
    
    from_stations_set, to_stations_set = train.getStations(from_city_pinyin,to_city_pinyin)
    for x in from_stations_set:
        print x
        addStation('6',x,from_city)
    
    print
    for x in to_stations_set:
        print x
        
    #print 'add complete'    
'''      



        