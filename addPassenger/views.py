#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.sessions.models import Session
from django.views.generic import TemplateView
# Create your views here.

def get_currentUser(request):
    s = Session.objects.get(pk=request.COOKIES['sessionid'])
    #print s.expire_date
    #print s.get_decoded()['_auth_user_id']
    user_id = s.get_decoded()['_auth_user_id']
    user = User.objects.get(id=user_id)
    return user

class Passenger_add(LoginRequiredMixin,TemplateView):
    #permission_required = "trainManage.add_train"
    template_name = "passenger_add.html"
    success_url = "/trainManage/"
    
    def get(self, request, *args, **kwargs):   
        currentUser = get_currentUser(request)
        print currentUser.username
        formSet = PassengerFormSet()

        return self.render_to_response(self.get_context_data(item_form=formSet,username=currentUser.username))

    def post(self, request, *args, **kwargs):
        currentUser = get_currentUser(request)
        formSet = PassengerFormSet(request.POST)
        
        if formSet.is_valid():
            for form in formSet:
                for k in form.cleaned_data:
                    if k=='passenger_name':
                        p_name = form.cleaned_data[k]
                    if k=='passenger_id':
                        p_id = form.cleaned_data[k]
                    if k=='student':
                        p_s = form.cleaned_data[k]
                p1 = Passenger.objects.filter(passenger_id=p_id)
                
                print p_name,
                print p_id,
                print p_s
              
                if len(print1)<1:
                   p1 = Passenger(passenger_name=p_name,passenger_id=p_id,student=p_s)
                   p1.save()
                   p1.users.add(currentUser)
                   p1.save()
              

            print formSet.total_form_count()
            print '-----------------------------'
           
            return HttpResponse('添加购票人成功！')

        else:
            return HttpResponse('添加失败！')

'''
class Passenger_add(CreateView):
    #permission_required = "trainManage.add_train"
    model = Passenger
    template_name = "passenger_add.html"
    success_url = "/trainManage/"
    form_class = PassengerForm

    def get(self, request, *args, **kwargs):
        self.object = None
        formSet = PassengerFormSet()
        return self.render_to_response(self.get_context_data(item_form=formSet))
    def post(self, request, *args, **kwargs):
        self.object = None
        formSet = PassengerFormSet(request.POST)
        
        if formSet.is_valid():
            for form in formSet:
                print form.cleaned_data['passenger_name']
            print formSet.total_form_count()
            print '-----------------------------'
           
            return HttpResponse('添加购票人成功！')

        else:
            return HttpResponse('添加失败！')
'''

    