# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from .models import Train, Run, Station
from .forms import TrainForm, RunForm
from django.forms import formset_factory
from datetime import datetime

# Create your views here.
def add_train(request):
    RunFormSet = formset_factory(RunForm, extra = 5)
    if request.method == "POST":
        trainForm = TrainForm(request.POST)
        runFormSet = RunFormSet(request.POST)
        if trainForm.is_valid() and runFormSet.is_valid():
            num_station = runFormSet.total_form_count()
            train = trainForm.save(commit=False)
            train.num_station = num_station

            day_count = 0
            runCount = -1
            time_list = []
            distance_list = []
            # 添加字段count_over_night, order_station
            for runForm in runFormSet:
                runCount += 1
                run = runForm.save(commit=False)
                arrive_time = datetime.strptime(run.arrive_time, "%H:%M")
                time_list.append(arrive_time)
                if(runCount != 0):
                    pre_arrive = time_list[runCount -1]
                    if arrive_time < pre_arrive:
                        day_count += 1
                station = Station.objects.get(station_name = run.station_name)
                run.station_name = station
                distance_list.append(run.distance_count)
                run.count_over_night = day_count
                run.run_key = Run(station.station_id, train.train_id)
                run.order_station = runCount 
                run.train_come_by = train
                run.save()
            train.train_type = train.train_id[0]
            train.distance = distance_list[-1]
            train.save()
            return HttpResponse("add done")
        return HttpResponse("wrong!")
            
    else:
        print('haha')
        trainForm = TrainForm()
        runFormSet = RunFormSet()
        return render(request, 'trainManage/add_train.html', {'form':trainForm, 'formset':runFormSet})
    



