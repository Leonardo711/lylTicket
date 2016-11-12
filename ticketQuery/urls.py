from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', ticketQuery.as_view(), name = "train_query"),
]
