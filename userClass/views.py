#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User,Group
from .forms import *
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse

##### Email validation ###
from itsdangerous import URLSafeSerializer as utsr
from itsdangerous import TimestampSigner
import base64

from django.conf import settings as django_settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sessions.models import Session

from addPassenger.models import Passenger
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from trainManage.models import *
from ticketQuery.models import *
from datetime import datetime
import pytz
from django.shortcuts import render_to_response

#from ticketQuery.models import Order



class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        timeStamp = TimestampSigner(self.security_key)
        username = timeStamp.sign(username)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        timeStamp = TimestampSigner(self.security_key)
        username = serializer.loads(token, salt = self.salt)
        username = timeStamp.unsign(username, max_age=expiration)
        print(username)
        return username


    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        timeStamp = TimestampSigner(self.security_key)
        username = serializer.loads(token, salt = self.salt)
        username = timeStamp.unsign(username)
        return username

# a global variable
token_confirm = Token(django_settings.SECRET_KEY)
# Create your views here.
class signup(TemplateView):
    form_class = SignUpForm
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        print request.GET
        return self.render_to_response(self.get_context_data(form = form))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(form = form))
        else:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = username
            try:
                user = User.objects.create_user(username = username, password=password, email=email)
            except:
                message="用户名已存在"
                return self.render_to_response(self.get_context_data(form=form, user_message=message))
            user.is_active = False
            user.save()
            token = token_confirm.generate_validate_token(username)
            message = "\n".join([u'欢迎注册lyl火车票预订系统', u'请访问该链接，完成邮箱验证:',
                                 "http://"+'/'.join([django_settings.DOMAIN, 'accounts','activate', token])])
            send_mail(u'注册用户验证信息', message,django_settings.EMAIL_HOST_USER, [email])
            user.groups.add(Group.objects.get(name="registedUser"))
            return render(request, "signUpSuccess.html")

def active_user(request, token):
    #print(token)
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
        return HttpResponse("对不起，验证链接已过期，请重新注册")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("对不起，您所验证的用户不存在，请重新注册")
    user.is_active = True
    user.save()
    return HttpResponse("验证完成")

#class signin(TemplateView):
#    form_class = SignInForm
#    template_name = "signin.html"
#
#    def get(self, request, *args, **kwargs):
#        form = self.form_class()
#        return self.render_to_response(self.get_context_data(form=form))
#
#    def post(self, request, *args, **kwargs):
#        form = self.form_class(request.POST)
#        if form.is_valid():
#            username = form.cleaned_data.get('username')
#            password = form.cleaned_data.get('password')
#            try:
#                userIn = User.objects.get(username=username,
#                                          password=password)
#            except:
#                loginErrorMessage = "用户名或密码错误"
#                print(request.POST)
#                return self.render_to_response(self.get_context_data(form=form, errorMessage=loginErrorMessage))
#            userIn.login()
#            print(request.POST)
#            return HttpResponseRedirect(request.POST['next'])
#        else:
#            loginErrorMessage = ''
#            print "unvalid", (request.POST)
#            return self.render_to_response(self.get_context_data(form=form, errorMessage=loginErrorMessage))

class passwordreset(TemplateView):
    form_class = PasswordResetForm
    template_name = "password_reset.html"
    def get(self, request, *args, **kwargs):
        form = PasswordResetForm()
        print request.GET
        return self.render_to_response(self.get_context_data(form = form))


    def post(self, request, *args, **kwargs):
        print "get post"
        form = self.form_class(request.POST)
        if not form.is_valid():
            print form.is_valid()
            return self.render_to_response(self.get_context_data(form = form))
        else:
            username = form.cleaned_data.get('username')
            email = username
            print username
            token = token_confirm.generate_validate_token(username)
            message = "\n".join([u'请访问该链接，完成密码重置:',
                                 "http://"+'/'.join([django_settings.DOMAIN, 'accounts','password_reset_confirm', token])])
            send_mail(u'密码重置', message,django_settings.EMAIL_HOST_USER, [email])

            #user.groups.add(Group.objects.get(name="registedUser"))
            return render(request, "resetEmailSended.html")
'''
class passwordresetconfirm(TemplateView):
    form_class = SignUpForm
    template_name = "password_reset_confirm.html"

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        print request.GET
        return self.render_to_response(self.get_context_data(form = form))
'''
        
def passwordresetconfirm(request, token):
    #print(token)
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
        return HttpResponse("对不起，重置密码链接已过期，请重新申请")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("对不起，您所验证的用户不存在，请重新注册")    

    if request.method=="GET":
        form = PasswordResetForm2()
        return render(request,'password_reset_confirm.html',{'form':form})

     
    if request.method=="POST":
        form = PasswordResetForm2(request.POST)
        if not form.is_valid():
            print form.is_valid()
            return self.render_to_response(self.get_context_data(form = form))
        else:
            password = form.cleaned_data.get('password')
            passwordagain = form.cleaned_data.get('passwordagain')
            if password!=passwordagain:
                return HttpResponse("对不起，两次密码不一致！")
            else:
                user.set_password(password)
                user.save()
                return HttpResponse("重置密码成功！")


         

  
    #return HttpResponse("验证完成")        
        
  

def get_currentUser(request):
    s = Session.objects.get(pk=request.COOKIES['sessionid'])
    #print s.expire_date
    #print s.get_decoded()['_auth_user_id']
    user_id = s.get_decoded()['_auth_user_id']
    user = User.objects.get(id=user_id)
    return user

class passwordchange(LoginRequiredMixin,TemplateView):

    form_class = PasswordChangeForm
    template_name = "password_change.html"

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm()
        print request.GET
        return self.render_to_response(self.get_context_data(form = form))

    def post(self, request, *args, **kwargs):
        currentUsr = get_currentUser(request)

        form = self.form_class(request.POST)

        if not form.is_valid():
            return self.render_to_response(self.get_context_data(form = form))
        else:
            originalpassword = form.cleaned_data.get('originalpassword')
            password = form.cleaned_data.get('password')
            passwordagain = form.cleaned_data.get('passwordagain')
            if currentUsr.check_password(originalpassword):
                if password==passwordagain:
                    currentUsr.set_password(password)
                    currentUsr.save()
                    return HttpResponse('修改密码成功！')
                else:
                    return HttpResponse('两次密码不一致!')
            else:
                return HttpResponse('原密码输入错误！')


class PersonInfo(LoginRequiredMixin,TemplateView):
    form_class = PassengerInfoForm
    template_name = "information.html"  

    def get(self, request, *args, **kwargs):
        pinfoformset = PassengerInfoFormSet()
        form_list = []
        user = get_currentUser(request)
        #order_set = Order.objects.filter(user_name=user.email)
        order_set = Order.objects.filter(user_name=user.username)
        for p in user.passenger_set.all():
            form_list.append(p)
            print p.passenger_name
        
        #update the order_staus
        for od in order_set:
            #cttime = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            cttime = datetime.now()
            #cttime.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
            tz = pytz.timezone('Asia/Shanghai')
            cttime = tz.localize(cttime)
            print cttime
            trip_date = od.trip_date
            dt = trip_date - cttime
            if dt.days<0 and od.order_status!=1:
                od.order_status = 1
                od.save() 
        
        return self.render_to_response(self.get_context_data(object_list = form_list,order_list=order_set))


class PassengerDelete(LoginRequiredMixin, DeleteView):
    model = Passenger
    template_name = "passenger_confirm_delete.html"
    success_url = '/accounts/personinfo/'

    # def get(self, request, *args, **kwargs):
    #     print "________________here_________________"
    #     print args
    #     print kwargs
    #     return HttpResponse('buyaogaoshi')

# def PassengerDelete(request, *args, **kwargs):
#     print request.GET
#     print request.POST

class PersonInfoOrder(LoginRequiredMixin,TemplateView):
    template_name = "personinfo_order_detail.html"
    def get(self, request, *args, **kwargs):
        order_id = kwargs['pk']
        print "order_id: ",
        print order_id
        od = Order.objects.get(order_id=order_id)
        #first to get the start station and end station order (int) from Run table
        start_station_ID = Station.objects.get(station_name=od.start_station).station_id
        end_station_ID = Station.objects.get(station_name=od.end_station).station_id
        print "-------------  Run order_of_station -----------------"
        Run_start_station = Run.objects.get(train_come_by_id = od.train_name,station_name_id = start_station_ID)
        order_of_start_station = Run_start_station.order_of_station
        print Run_start_station.order_of_station
        Run_end_station = Run.objects.get(train_come_by_id=od.train_name,station_name_id = end_station_ID)
        order_of_end_station = Run_end_station.order_of_station
        print Run_end_station.order_of_station
        print "-------------  Run  order_of_station-----------------"
        
        start_time = Run_start_station.arrive_time
        end_time = Run_end_station.arrive_time
        distance = Run_end_station.distance_count - Run_start_station.distance_count
    

        print "-----------start_end_time and distance-------"
        print start_time,end_time,distance
        print "-----------start_end_time and distance-------"
        otherinfo = {}
        otherinfo['start_date'] = od.trip_date.strftime("%Y/%m/%d")
        otherinfo['start_time'] = start_time
        otherinfo['end_time'] = end_time
        otherinfo['distance'] = distance
        seat_type_dict = {'shangwu': '商务座',
        'yideng': '一等座',
        'erdeng': '二等座',
        'ruanwo': '软卧',
        'yingwo': '硬卧',
        'yingzuo': '硬座',
        }

        otherinfo['seat_type'] = seat_type_dict[od.seat.carriage.seat_type]
        otherinfo['order_of_start_station'] = order_of_start_station
        otherinfo['order_of_end_station'] = order_of_end_station

        #cttime = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
        cttime = datetime.now()
        #cttime.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        tz = pytz.timezone('Asia/Shanghai')
        cttime = tz.localize(cttime)
        print cttime
        trip_date = od.trip_date
        
        print trip_date
        
        dt = trip_date - cttime 
        print dt.days,dt.total_seconds()
        timeinfo = {}
        timeinfo['days'] = dt.days
        timeinfo['total_seconds'] = dt.total_seconds()
        timeinfo['total_hours'] = dt.total_seconds()/3600
        timeinfo['hours'] = int(timeinfo['total_hours']) - timeinfo['days']*24
        timeinfo['minutes'] = int((timeinfo['total_seconds'] - int(timeinfo['total_hours'])*3600)/60)
        timeinfo['seconds'] = timeinfo['total_seconds'] - int(timeinfo['total_hours'])*3600 - timeinfo['minutes']*60 

        if dt.days<0 and od.order_status!=1:
            od.order_status = 1
            od.save()

        return self.render_to_response(self.get_context_data(order = od,otherinfo=otherinfo,timeinfo=timeinfo))

class OrderDelete(LoginRequiredMixin,TemplateView):
    template_name = "order_confirm_delete.html"
    success_url = '/accounts/personinfo/'
    def get(self, request, *args, **kwargs):
        order_id = kwargs['pk']
        print "order_id: ",
        print order_id
        od = Order.objects.get(order_id=order_id)
        return self.render_to_response(self.get_context_data(object = od))

    def post(self, request, *args, **kwargs):
        order_id = request.POST['order_id']
        print "Post order_id: ",
        print order_id
        try:
            od = Order.objects.get(order_id=order_id)

            #first to get the start station and end station order (int) from Run table
            start_station_ID = Station.objects.get(station_name=od.start_station).station_id
            end_station_ID = Station.objects.get(station_name=od.end_station).station_id
            Run_start_station = Run.objects.get(train_come_by_id = od.train_name,station_name_id = start_station_ID)
            order_of_start_station = Run_start_station.order_of_station
            Run_end_station = Run.objects.get(train_come_by_id=od.train_name,station_name_id = end_station_ID)
            order_of_end_station = Run_end_station.order_of_station

            #recover the seat status
            seat = od.seat
            status_list = list(seat.status)
            status_list[order_of_start_station-1:order_of_end_station-1]=u'1'*(order_of_end_station-order_of_start_station)
            seat.status = ''.join(status_list)
            seat.save()
            od.delete()
            response = "退票成功!"
        except:
            response ="票信息不存在"
        return render_to_response('ticketQuery/ticket_order_completed.html', context={'response':response})

