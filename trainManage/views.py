# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Train, Run, Station, Carriage,Seat
from .forms import *
from django.forms import formset_factory
from datetime import datetime
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

timeSpan = 3 # 卖票的时间跨度
# Create your views here.
class train_ListView(PermissionRequiredMixin, ListView):
    permission_required = "trainManage.add_train"
    model = Train
    template_name = 'trainManage/train_list.html'

class train_create(PermissionRequiredMixin, CreateView):
    permission_required = "trainManage.add_train"
    model = Train
    template_name = "trainManage/train_create.html"
    success_url = "/trainManage/"
    form_class = TrainForm


    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form =self.get_form(form_class)
        fileForm = trainFileForm()
        run_form = RunForm_stationSet()
        return self.render_to_response(self.get_context_data(form=form, item_form=run_form, trainFileForm=trainFileForm))

    def post(self, request, *args, **kwargs):
        print(type(self.request.POST))
        self.object=None
        form_class = self.get_form_class()
        form =self.get_form(form_class)
        run_form = RunForm_stationSet(request.POST)
        if (form.is_valid() and run_form.is_valid() ):
            num_station = run_form.total_form_count()
            train = form.save(commit=False)
            self.object=train
            train.num_station = num_station
            day_count = 0
            time_list = []
            distance_list = []
            print(len(run_form))
            for runForm in run_form:
                run = runForm.save(commit=False)
                distance_list.append(run.distance_count)
            train.train_type = train.train_id[0]
            train.distance = distance_list[-1]
            train.save()
            for runForm in run_form:
                run = runForm.save(commit=False)
                runCount = run.order_of_station
                #arrive_time = datetime.strptime(run.arrive_time, "%H:%M")
                arrive_time = run.arrive_time
                time_list.append(arrive_time)
                if(runCount != 1):
                    pre_arrive = time_list[runCount -1]
                    if arrive_time < pre_arrive:
                        day_count += 1
                run.count_over_night = day_count
                run.run_key = Run.generateRunKey(run.station_name.station_id, train.train_id)
                print("here is no problem")
                run.train_come_by = train
                print(run.count_over_night)
                print(run.run_key)
                print(run.order_station)
                run.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            print("wrong validation")
            return self.render_to_response(
                    self.get_context_data(form=form,
                        item_form=run_form))


class train_detail(PermissionRequiredMixin,DetailView):
    permission_required = "trainManage/add_train"
    model = Train
    template_name = "trainManage/train_detail.html"
    context_object_name = "train"

class train_delete(PermissionRequiredMixin, DeleteView):
    permission_required = "trainManage/add_train"
    model = Train
    template_name = "trainManage/train_confirm_delete.html"
    success_url = '/trainManage/'


class addCarriage(PermissionRequiredMixin, CreateView):
    permission_required = "trainManage.add_train"
    model = Train
    template_name = "trainManage/addCarriage.html"
    success_url = "/trainManage/"


    def get(self, request, *args, **kwargs):
        self.object = Train.objects.get(train_id = kwargs['pk'])
        carriage_form = CarriageForm()
        return self.render_to_response(self.get_context_data(form=self.object, item_form=carriage_form))

    def post(self, request, *args, **kwargs):
        print(request)
        self.object = Train.objects.get(train_id = kwargs['pk'])
        carriage_form = CarriageForm(request.POST)
        if ( carriage_form.is_valid() ):
            status = '1'*self.object.num_station
            train_id = self.object
            for carriageform in carriage_form:
                carriage = carriageform.save(commit=False)
                carriage.train_id = self.object
                carriage.carriage_key = Carriage.generateCarriageKey(self.object.train_id, carriage.carriage_id)
                carriage.save()
                for seat_id in range(1, carriage.num_seat+1):
                    for i in range(timeSpan):
                        print(i)
                        date = datetime.date(datetime.today()+timedelta(i))
                        seat_key = Seat.generateSeatRunKey(date, carriage.carriage_key, seat_id)
                        print(seat_key)
                        seat = Seat(seat_key = seat_key,
                                    carriage=carriage,
                                    seat_id = seat_id,
                                    date=date,
                                    status=status)
                        print("nothing wrong here")
                        seat.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            print("wrong validation")
            return self.render_to_response(
                self.get_context_data(form=self.object,
                                      item_form=carriage_form))

def trainCreateFromFile(request):
    if request.method == "POST":
        file = request.FILES['file']
        ex_order = 0
        distance_list = []
        station_list = []
        arrive_time_list = []
        ex_train = ''
        for line in  request.FILES['file']:
            try:
                train_id, order, station_name, arrive_time, distance = line.strip().split("\t")
            except:
                return HttpResponse("Wrong file")
            order = int(order)
            distance = float(distance)
            day_count  = 0
            if  ex_order < order:
                ex_train = train_id
                ex_order = order
                distance_list.append(distance)
                try:
                    station_list.append(Station.objects.get(station_name = station_name))
                except:
                    print station_name
                    return HttpResponseRedirect("/")
                arrive_time_list.append(arrive_time)
            else:
                train = Train()
                train.distance = distance_list[-1]
                train.train_id = ex_train
                train.train_type = train_id[0]
                train.num_station = ex_order
                train.save()
                for i in range(ex_order):
                    run = Run()
                    runCount = i+1;
                    if(runCount != 1):
                        pre_arrive = arrive_time_list[runCount -1]
                        if arrive_time < pre_arrive:
                            day_count += 1
                    run.count_over_night = day_count
                    run.run_key = Run.generateRunKey(station_list[i].station_id, train.train_id)
                    run.order_of_station = runCount
                    run.station_name = station_list[i]
                    run.arrive_time = arrive_time_list[i]
                    run.distance_count = distance_list[i]
                    run.train_come_by = train
                    run.save()
                ex_order = 1
                distance_list=[distance]
                station_list=[Station.objects.get(station_name = station_name)]
                arrive_time_list = [arrive_time]
                day_count = 0
                run.save()
        train = Train()
        train.distance = distance_list[-1]
        train.train_id = ex_train
        train.train_type = train_id[0]
        train.num_station = ex_order
        train.save()
        day_count  = 0
        for i in range(ex_order):
            run = Run()
            runCount = i+1;
            if(runCount != 1):
                pre_arrive = arrive_time_list[runCount -1]
            if arrive_time < pre_arrive:
                day_count += 1
            run.count_over_night = day_count
            run.run_key = Run.generateRunKey(station_list[i].station_id, train.train_id)
            run.order_station = runCount
            run.train_come_by = train
            run.save()
    else:
        print('wrong')
    return HttpResponseRedirect("/trainManage/create/")

def load(file):
    for line in (open("station_city_set.txt", 'r')):
        station_id, station_name, station_city = line.strip().split("\t")
        station = Station.objects.create(station_id=int(station_id), station_name=station_name,station_city=station_city)
        station.save()
