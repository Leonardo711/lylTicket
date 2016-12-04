# -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
#from django.views.generic import View
from django.views.generic.base import TemplateView
from .forms import *
from trainManage.models import *
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
        query = Query(startStation, endStation, date)
        resultSet= query.search()
        print resultSet
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
        print "收到提交！"
        start = request.POST['start']
        end = request.POST['end']
        date = request.POST['date']
        date = datetime.date(datetime.strptime(date, "%b. %d, %Y"))
        print(date)
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
                    seat_key_set = seat_type_to_seat_key.setdefault(seat_type, [])
                    seat_key_set.append(seat_key)
            except:
                pass

      
        user = get_currentUser(request)
        passenger_set = user.passenger_set.all()
        for p in passenger_set:
            print p.passenger_name
        #print seat_type_to_seat_key

        # they are all strings , not objects
        return self.render_to_response(self.get_context_data(seat_type_to_seat_key=seat_type_to_seat_key,
                                                             train_id = train_id,
                                                             date=date,
                                                             start=start,
                                                             end = end,passenger_set=passenger_set))

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
            startDate = self.date - timedelta(startRun.count_over_night) # the start date of train
            if today< self.date or ( today==self.date and datetime.time(datetime.now()) < startRun.arrive_time): # before train arrive
            # input time must later than now
                if  startOrder < endOrder:
                    arrive_time = \
                        train.run_set.get(train_come_by=train,station_name=self.start).arrive_time
                    resultSet[train.train_id] = {'yideng':[],'erdeng':[],'shangwu':[],'ruanwo':[],
                                                 'yingzuo':[],'yingzuo':[],'wuzuo':[], "arrive_time":arrive_time}
                    trainStartTime[train.train_id]= \
                        train.run_set.get(train_come_by=train,station_name=self.start).arrive_time
                    for carriage in train.carriage_set.all():
                        seatSet = carriage.seat_set.all()
                        seatSet = seatSet.filter(date=startDate)
                        for seat in seatSet:
                            if seat.status[startOrder-1:endOrder] == "1" *(endOrder-startOrder+1):
                                type_seat = resultSet.setdefault(train.train_id,{})
                                seat_result = type_seat.setdefault(seat.carriage.seat_type,[])
                                seat_result.append(seat)
        return resultSet


class ticketOrderConfirm(TemplateView, LoginRequiredMixin):
    template_name = "ticketQuery/ticket_order_confirm.html"
    def post(self, request):
        order_id = '111111'
        passenger_name = request.POST['passenger_name']
        passenger_id = request.POST['passenger_id']
        passenger_tel = request.POST['tel']
        start_time = request.POST['time']
        train_id = request.POST['train_id']
        start_station = request.POST['start']
        end_station = request.POST['end']
        print order_id,train_id,passenger_name,passenger_id,passenger_tel,start_time,start_station,end_station
       # info_dict = {'order_id':order_id,'passenger_name':passenger_name,'passenger_id',passenger_id,'passenger_tel':passenger_tel,'start_time':start_time,'train_id':train_id,'start_station':start_station,'end_station':end_station}
        info_dict = {}
        info_dict['order_id'] = order_id
        info_dict['passenger_name'] = passenger_name
        info_dict['passenger_id'] = passenger_id
        info_dict['passenger_tel'] = passenger_tel
        info_dict['start_time'] = start_time
        info_dict['train_id'] = train_id
        info_dict['start_station'] = start_station
        info_dict['end_station'] = end_station
        info_dict_list = []
        info_dict_list.append(info_dict)
        # they are all strings , not objects
        return render_to_response(self.get_context_data(obj = info_dict))