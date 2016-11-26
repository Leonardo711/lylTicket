from django.conf.urls import url, include
#from . import views
from .views import *

urlpatterns = [
#        url(r'^add_train/$', add_train, name = "add_train"),
        url(r'^$', Passenger_add.as_view(), name = "passenger_add"),
      
        ]