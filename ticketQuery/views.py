# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
#from django.views.generic import View
from django.views.generic.base import TemplateView
from .forms import *
from trainManage.models import *
from ticketQuery.models import *
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from collections import OrderedDict
#from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User,Group
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect




def get_currentUser(request):
    s = Session.objects.get(pk=request.COOKIES['sessionid'])
    #print s.expire_date
    #print s.get_decoded()['_auth_user_id']
    user_id = s.get_decoded()['_auth_user_id']
    user = User.objects.get(id=user_id)
    return user




# Create your views here.
class ticketQuery(TemplateView):
    form_class = TicketQueryForm
    template_name = "ticketQuery/ticket_query.html"
    def get(self, request, *args, **kwargs):
        form = TicketQueryForm()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        request.session['test'] = False;
        form = self.form_class(request.POST)
        startStationID = request.POST['startStation']
        startStation = Station.objects.get(station_id=startStationID)
        endStationID = request.POST['endStation']
        endStation = Station.objects.get(station_id=endStationID)
        date =  datetime.strptime(request.POST['date'], "%m/%d/%Y")
        date = datetime.date(date)
        query = Query(startStation, endStation, TimeSpan(time=date))
        print('below here')
        resultSet= query.search()
        print('below here')
        #print resultSet
        return self.render_to_response(self.get_context_data(form=form,
                                                             startStation=startStation,
                                                             endStation=endStation,
                                                             date = date,
                                                             resultSet=resultSet,
                                                             ))

class ticketOrder(TemplateView, LoginRequiredMixin):
    template_name = "ticketQuery/ticket_order.html"
    def post(self, request):
        # rebuild the result to a dictionary which store the result
        seat_type_to_seat_key = {}
        train_id = request.POST['train_id']
        seat_type_dict = {'shangwu': '商务座',
        'yideng': '一等座',
        'erdeng': '二等座',
        'ruanwo': '软卧',
        'yingwo': '硬卧',
        'yingzuo': '硬座',
        }
        start = request.POST['start']
        end = request.POST['end']
        date = request.POST['date']
        date = datetime.date(datetime.strptime(date, "%b. %d, %Y"))
        print(request.POST)
        print(request.session.keys())
        seat_type_num = request.POST['seat_type_num']
        for i in range(1, int(seat_type_num)+1):
            seat_type_index = "seat_type_" + str(i)
            try:
                seat_type = request.POST[seat_type_index]
                seat_type_counter_index = seat_type + "_counter"
                seat_type_counter = request.POST[seat_type_counter_index]
                for j in range(1, int(seat_type_counter)+1):
                    seat_index = seat_type +"_" + str(j)
                    seat_key = request.POST[seat_index]
                    seat_key_set = seat_type_to_seat_key.setdefault(seat_type_dict[seat_type], [])
                    seat_key_set.append(seat_key)
            except:
                pass
        user = get_currentUser(request)
        passenger_set = user.passenger_set.all()
        for p in passenger_set:
            print p.passenger_name
        #print seat_type_to_seat_key
        form_set = PassengerInfoFormSet()
        # they are all strings , not objects
        return self.render_to_response(self.get_context_data(seat_type_to_seat_key=seat_type_to_seat_key,
                                                             train_id = train_id,
                                                             date=date,
                                                             start=start,
                                                             end = end,
                                                             passenger_set=passenger_set,
                                                             form_set=form_set))

# This is a class for search process
class Query(object):
    def __init__(self, start, end, date):
        self.start =  start
        self.end = end
        self.date = date
        self.delay = 30 # the time you can order ticket before the
    def search(self):
        #resultSet = {train_id:{seat_type:[seat_key]}}
        resultSet = {}
        startSet = set()
        endSet = set()
        for run in self.start.run_set.all():
            startSet.add(run.train_come_by)
        for run in self.end.run_set.all():
            endSet.add(run.train_come_by)
        trainSet = startSet & endSet
        trainStartTime = {}

        for train in trainSet:
            startRun = Run.objects.get(train_come_by= train, station_name=self.start)
            endRun = Run.objects.get(train_come_by=train, station_name=self.end)
            startOrder = startRun.order_of_station
            endOrder = endRun.order_of_station
            today = datetime.date(datetime.today())
            startDate = self.date.time - timedelta(startRun.count_over_night) # the start date of train
            if today< self.date.time or ( today==self.date.time and datetime.time(datetime.now()) < startRun.arrive_time): # before train arrive
            # input time must later than now
                if  startOrder < endOrder:
                    arrive_time = \
                        train.run_set.get(train_come_by=train,station_name=self.start).arrive_time
                    resultSet[train.train_id] = {'yideng':[],'erdeng':[],'shangwu':[],'ruanwo':[],
                                                 'yingzuo':[],'yingzuo':[], "arrive_time":arrive_time}
                    trainStartTime[train.train_id]= \
                        train.run_set.get(train_come_by=train,station_name=self.start).arrive_time
                    for carriage in train.carriage_set.all():
                        seatSet = carriage.seat_set.all()
                        seatSet = seatSet.filter(date=TimeSpan(time=startDate))
                        for seat in seatSet:
                            if seat.status[startOrder-1:endOrder] == "1" *(endOrder-startOrder+1):
                                type_seat = resultSet.setdefault(train.train_id,{})
                                seat_result = type_seat.setdefault(seat.carriage.seat_type,[])
                                seat_result.append(seat)
        
        resultSet = OrderedDict(sorted(resultSet.iteritems(), key=lambda x:x[1]))
        return resultSet


class ticketOrderConfirm(TemplateView, LoginRequiredMixin):
    template_name = "ticketQuery/ticket_order_confirm.html"
    def post(self, request):
        print request.POST
        order_id = '111111'
        total_forms = request.POST['form-TOTAL_FORMS']
        print "total_forms = " + total_forms
        print int(total_forms)

        total_passenger = request.POST['total_passenger']
        print "total_passenger = " + total_passenger

        seat_counter = {}
        seat_used_counter = {}
        seat_type_num = request.POST['seat_type_num']
        print "-------------seat_type information-------------"
        for i in range(1, int(seat_type_num)+1):
            seat_type_index = "seat_type_" + str(i)
            try:
                seat_type = request.POST[seat_type_index]
                seat_type_counter_index = seat_type + "_counter"
                seat_type_counter = request.POST[seat_type_counter_index]
                seat_counter[seat_type] = int(seat_type_counter)
                seat_used_counter[seat_type] = 0
                print 'seat_type: ' + seat_type + ' seat_type_counter:' + str(seat_counter[seat_type])
                print 'seat_type: ' + seat_type + ' seat_used_counter:' + str(seat_used_counter[seat_type])
            except:
                pass
        print "-------------seat_type information-------------"
        '''
        yideng_counter = request.POST[u'一等座_counter']
        erdeng_counter = request.POST[u'二等座_counter']
        shangwu_counter = request.POST[u'商务座_counter']
        yingzuo_counter = request.POST[u'硬座_counter']
        yingwo_counter = request.POST[u'硬卧_counter']
        ruanwo_counter = request.POST[u'软卧_counter']

        seat_counter = {u'一等座':int(yideng_counter),u'二等座':int(erdeng_counter),u'商务座':int(shangwu_counter),\
                        u'硬座':int(yingzuo_counter),u'硬卧':int(yingwo_counter),u'软卧':int(ruanwo_counter)}

        '''
        '''
        seat1 = Seat.objects.get(seat_key=seat_key_1[2:])
        print "---------------seat information----------------  "
        print seat1.carriage.train_id,seat1.carriage.carriage_id,seat1.seat_id,seat1.carriage.seat_type,seat1.date,seat1.status
        print "---------------seat information----------------  "
        '''
        #process each passenger
        passenger_info_list = []
        seat_list = []
        '''
        seat_used_counter = {u'一等座':0,u'二等座':0,u'商务座':0,\
                        u'硬座':0,u'硬卧':0,u'软卧':0}
        '''
        for i in xrange(0,int(total_forms)):
            key_order = "form-%d-order" % i
            key_seattype = "form-%d-seat_type" % i
            key_student = "form-%d-student" % i
            key_name = "form-%d-passenger_name" % i
            key_id = "form-%d-passenger_id" % i
            key_phone = "form-%d-passenger_phone" % i
            #key_set = [key_order,key_seattype,key_student,key_name,key_id,key_phone]
            passenger_info = {}
            passenger_info['order'] = request.POST[key_order]
            passenger_info['seat_type'] = request.POST[key_seattype]
            passenger_info['student'] = request.POST[key_student]
            print "---------  student  ---------"
            print passenger_info['student']
            print "---------  student  ---------"
            passenger_info['passenger_name'] = request.POST[key_name]
            passenger_info['passenger_id'] = request.POST[key_id]
            passenger_info['passenger_phone'] = request.POST[key_phone]
            passenger_info['start_station'] = request.POST['start']
            passenger_info['end_station'] = request.POST['end']
            passenger_info['date'] = request.POST['date']
            passenger_info['train_id'] = request.POST['train_id']




            #for key in passenger_info:
            #    print passenger_info[key],
            seat_used_counter[passenger_info['seat_type']] = seat_used_counter[passenger_info['seat_type']]+1
            if seat_used_counter[passenger_info['seat_type']]<=seat_counter[passenger_info['seat_type']]:
                #generate seat_key_str : "一等座_1"
                seat_key_str = passenger_info['seat_type']+'_'+str(seat_used_counter[passenger_info['seat_type']])
                print seat_key_str
                #get seat_key, the seat_key has two useless space:u'  G123XXXXXX',from the third letter
                seat_key = request.POST[seat_key_str]
                #get seat from datebase
                seat = Seat.objects.get(seat_key=seat_key[2:])
                seat.carriage.carriage_id,seat.seat_id
                passenger_info['carriage_id'] = seat.carriage.carriage_id
                passenger_info['seat_id'] = seat.seat_id
                passenger_info['seat_key'] = seat.seat_key
            else:
                print "current seat_type " + passenger_info['seat_type'] + " is full."


            #generate order_id : date + train_id + carriage_id + seat_id + passenger_id[-4:]
            d = {'G':'1','D':'2','K':'3','Z':'4'}
            train_id_2 = d[passenger_info['train_id'][0]]+passenger_info['train_id'][1:]
            #print "train_id_2 : " + train_id_2
            order_id = passenger_info['date'].replace('/','') +  train_id_2 + passenger_info['passenger_id'][-4:]
            passenger_info['order_id'] = order_id

            #calculate the price
            p = Price.objects.get(train_type=passenger_info['train_id'][0],seat_type=passenger_info['seat_type'])
            ratio_student = p.ratio_student
            price_per_km = p.price_per_km
            start_station_ID = Station.objects.get(station_name=passenger_info['start_station']).station_id
            end_station_ID = Station.objects.get(station_name=passenger_info['end_station']).station_id
            print "-------------  Run  -----------------"
            Run_start_station = Run.objects.get(train_come_by_id = passenger_info['train_id'],station_name_id = start_station_ID)
            print Run_start_station.arrive_time
            Run_end_station = Run.objects.get(train_come_by_id=passenger_info['train_id'],station_name_id = end_station_ID)
            print Run_end_station.arrive_time
            print "-------------  Run  -----------------"

            distance = Run_end_station.distance_count - Run_start_station.distance_count

            if passenger_info['student']=='1':
                price = ratio_student * distance * price_per_km
            else:
                price = distance * price_per_km
            print "price is :" + str(price)
            passenger_info['price'] = price
            passenger_info['time'] = Run_start_station.arrive_time
            passenger_info_list.append(passenger_info)
            seat_list.append(seat)

        print passenger_info_list
        passenger_num = len(passenger_info_list)
        print "passenger_num = " + str(passenger_num)

        passenger_info_set = PassengerInfoFormSet(request.POST)
        print
        print '--------------passenger info-----------------'
        passenger_counter = 0
        for passenger in passenger_info_set:
            #print passenger.['order'],passenger.['student'],
            #print passenger.cleaned_data['passenger_name'],
            #print passenger.cleaned_data['passenger_id'],
            #print passenger.cleaned_data['passenger_phone']
            passenger_counter = passenger_counter + 1
        print "passenger_counter： " + str(passenger_counter)
        print '--------------passenger info-----------------'
        print
        usr = get_currentUser(request)
        # they are all strings , not objects
        return render_to_response("ticketQuery/ticket_order_confirm.html",{'user':usr,'p_info_list':passenger_info_list,'passenger_num':passenger_num})


class ticketOrderCompleted(TemplateView, LoginRequiredMixin):
    template_name = "ticketQuery/ticket_order_completed.html"
    def post(self, request):
        print "----------------  POST  -----------------"
        print request.POST
        print "----------------  POST  -----------------"
        passenger_num_str = request.POST["passenger_num"]
        passenger_num = int(passenger_num_str)
        print "有%d个乘客" % passenger_num
        passenger_info_list = []
        for i in xrange(1,passenger_num+1):
            key_order_id = "order_id_"+str(i)
            key_seat_type = "seat_type_"+str(i)
            key_student = "student_"+str(i)
            key_passenger_name = "passenger_name_"+str(i)
            key_passenger_id = "passenger_id_"+str(i)
            key_passenger_phone = "passenger_phone_"+str(i)
            key_train_id = "train_id_"+str(i)
            key_carriage_id = "carriage_id_"+str(i)
            key_seat_id = "seat_id_"+str(i)
            key_date = "date_"+str(i)
            key_time = "time_"+str(i)
            key_start_staion = "start_station_"+str(i)
            key_end_station = "end_station_"+str(i)
            key_price = "price_"+str(i)
            key_seat_key = "seat_key_"+str(i)

            #get seat_key
            key_set = [key_order_id,key_seat_type,key_student,key_passenger_name,key_passenger_id,\
            key_passenger_phone,key_train_id,key_carriage_id,key_seat_id,key_date,key_time,\
            key_start_staion,key_end_station,key_price,key_seat_key]

            passenger_info = {}
            for key in key_set:
                #process the key first, remove the str(i) infomation and '_'
                passenger_info[key.replace(str(i),'')[0:-1]] = request.POST[key]
            #print passenger_info

            #add to list
            passenger_info_list.append(passenger_info)

            order_id = passenger_info['order_id']
            train_name = Train.objects.get(train_id=passenger_info['train_id'])
            start_station = Station.objects.get(station_name=passenger_info['start_station'])
            end_station = Station.objects.get(station_name=passenger_info['end_station'])
            seat = Seat.objects.get(seat_key=passenger_info['seat_key'])
            trip_date = passenger_info['date']
            pay = passenger_info['price']
            passenger_name = passenger_info['passenger_name']
            passenger_id = passenger_info['passenger_id']
            student = passenger_info['student']
            #The phone field in model is Integer
            passenger_phone = passenger_info['passenger_phone']

            order_time = datetime.now()

            usr = get_currentUser(request)
            user_name = usr.username

            #now update the status of seat
            #first to get the start station and end station order (int) from Run table
            start_station_ID = Station.objects.get(station_name=passenger_info['start_station']).station_id
            end_station_ID = Station.objects.get(station_name=passenger_info['end_station']).station_id
            print "-------------  Run order_of_station -----------------"
            Run_start_station = Run.objects.get(train_come_by_id = passenger_info['train_id'],station_name_id = start_station_ID)
            order_of_start_station = Run_start_station.order_of_station
            print Run_start_station.order_of_station
            Run_end_station = Run.objects.get(train_come_by_id=passenger_info['train_id'],station_name_id = end_station_ID)
            order_of_end_station = Run_end_station.order_of_station
            print Run_end_station.order_of_station
            print "-------------  Run  order_of_station-----------------"
            arrive_time = Run_start_station.arrive_time

            
            #dt.date(passenger_info['date'])
            print str(passenger_info['date'])+" "+arrive_time.strftime("%H:%M:%S")
            dt = datetime.strptime(str(passenger_info['date'].replace('/','-'))+" "+arrive_time.strftime("%H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            print dt
            
            trip_date = dt

            print
            #get the status of the seat
            #print "seat status: " + str(seat.date.time)+" "+str(seat.carriage.carriage_id)+" "+str(seat.seat_id)+" "+seat.status
            #update the status of start_staion to end_staion-1,the end_station should not be changed
            status_list = list(seat.status)
            status_list[order_of_start_station-1:order_of_end_station]=u'0'*(order_of_end_station-order_of_start_station+1)
            seat.status = ''.join(status_list)
            #print "update seat status: " + str(seat.date.time)+" "+str(seat.carriage.carriage_id)+" "+str(seat.seat_id)+" "+seat.status
            seat.save()

            try:
                od = Order.objects.create(order_id=order_id,user_name=user_name,passenger_name=passenger_name,\
                passenger_id=passenger_id,passenger_phone=passenger_phone,student=student,\
                order_time=order_time,train_name=train_name,start_station=start_station,end_station=end_station,\
                trip_date=trip_date,seat=seat,pay=pay)
                od.save()
            except Exception, e:
                print e
                status_list = list(seat.status)
                status_list[order_of_start_station-1:order_of_end_station]=u'1'*(order_of_end_station-order_of_start_station+1)
                seat.status = ''.join(status_list)
                seat.save()
                return HttpResponse("单人每车次限购一张票!")
            else:
                pass
            finally:
                pass

            


        return HttpResponse("购票成功!")
