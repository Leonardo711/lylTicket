from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', ticketQuery.as_view(), name = "ticket_query"),
    url(r'^order/$', ticketOrder.as_view(), name="ticket_order"),
    url(r'^order/orderconfirm/$', ticketOrderConfirm.as_view(), name="ticket_order_confirm"),
]
