# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import Train, Run, Station
from .forms import *
from django.forms import formset_factory
from datetime import datetime

# Create your views here.
class train_ListView(ListView):
    model = Train
    template_name = 'train_list.html'

class train_create(CreateView):
    model = Train
    template_name = "train_create.html"
    success_url = "/trainManage/"
    form_class = TrainForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form =self.get_form(form_class)
        run_form = RunForm_stationSet()
        return self.render_to_response(self.get_context_data(form=form, item_form=run_form))

    def post(self, request, *args, **kwargs):
        self.object=None
        form_class = self.get_form_class()
        form =self.get_form(form_class)
        run_form = RunForm_stationSet(self.request.POST)
        if (form.is_valid() and run_form.is_valid()):
            num_station = run_form.total_form_count()
            train = form.save(commit=False)
            self.object=train
            train.num_station = num_station

          #  day_count = 0
          #  runCount = -1
          #  time_list = []
            distance_list = [9]
            print(distance_list)
          #  for runForm in run_form:
          #      runCount += 1
          #      run = runForm.save(commit=False)
          #      arrive_time = datetime.strptime(run.arrive_time, "%H:%M")
          #      time_list.append(arrive_time)
          #      if(runCount != 0):
          #          pre_arrive = time_list[runCount -1]
          #          if arrive_time < pre_arrive:
          #              day_count += 1
          #      station = Station.objects.get(station_name = run.station_name)
          #      run.station_name = station
          #      distance_list.append(run.distance_count)
          #      run.count_over_night = day_count
          #      run.run_key = Run(station.station_id, train.train_id)
          #      run.order_station = runCount 
          #      run.train_come_by = train
          #      print(run.count_over_night)
          #      print(run.run_key)
          #      print(run.order_station)
          #      run.save()
            train.train_type = train.train_id[0]
            train.distance = distance_list[-1]
            train.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                    self.get_context_data(form=form,
                        run_form=run_form))


#
#def add_train(request):
#    RunFormSet = formset_factory(RunForm, extra = 5)
#    if request.method == "POST":
#        trainForm = TrainForm(request.POST)
#        runFormSet = RunFormSet(request.POST)
#        if trainForm.is_valid() and runFormSet.is_valid():
#            num_station = runFormSet.total_form_count()
#            train = trainForm.save(commit=False)
#            train.num_station = num_station
#
#            day_count = 0
#            runCount = -1
#            time_list = []
#            distance_list = []
#            # 添加字段count_over_night, order_station
#            for runForm in runFormSet:
#                runCount += 1
#                run = runForm.save(commit=False)
#                arrive_time = datetime.strptime(run.arrive_time, "%H:%M")
#                time_list.append(arrive_time)
#                if(runCount != 0):
#                    pre_arrive = time_list[runCount -1]
#                    if arrive_time < pre_arrive:
#                        day_count += 1
#                station = Station.objects.get(station_name = run.station_name)
#                run.station_name = station
#                distance_list.append(run.distance_count)
#                run.count_over_night = day_count
#                run.run_key = Run(station.station_id, train.train_id)
#                run.order_station = runCount 
#                run.train_come_by = train
#                run.save()
#            train.train_type = train.train_id[0]
#            train.distance = distance_list[-1]
#            train.save()
#            return HttpResponse("add done")
#        if not runFormSet.is_valid():
#            return HttpResponse("formset wrong!")
#        return HttpResponse("train form  wrong!")
#            
#    else:
#        trainForm = TrainForm(prefix="Train")
#        runFormSet = RunFormSet(prefix="Run")
#        return render(request, 'trainManage/add_train.html', {'form':trainForm, 'formset':runFormSet})
