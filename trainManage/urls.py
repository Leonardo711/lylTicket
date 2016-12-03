from django.conf.urls import url, include
#from . import views
from .views import *

urlpatterns = [
#        url(r'^add_train/$', add_train, name = "add_train"),
        url(r'^$', train_ListView.as_view(), name = "train_list"),
        url(r'^create/$', train_create.as_view(), name = "train_create"),
        url(r'^detail/(?P<pk>[\w]+)$', train_detail.as_view(), name="train_detail"),
        url(r'^delete/(?P<pk>[\w]+)$', train_delete.as_view(), name="train_delete"),
        url(r'^addCarriage/(?P<pk>[\w]+)$', addCarriage.as_view(), name="train_delete"),
        url(r'^trainCreateFromFile/$', trainCreateFromFile, name="train_create_file"),
        ]

