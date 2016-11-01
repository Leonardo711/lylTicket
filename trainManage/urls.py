from django.conf.urls import url, include
#from . import views
from .views import *

urlpatterns = [
#        url(r'^add_train/$', add_train, name = "add_train"),
        url(r'^$', train_ListView.as_view(), name = "train_list"),
        url(r'^create/$', train_create.as_view(), name = "train_create"),
        ]

