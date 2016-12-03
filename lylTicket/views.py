from django.shortcuts import render
from django.views.generic import TemplateView
from ticketQuery.forms import TicketQueryForm

def index(request):
    form = TicketQueryForm()
    return render(request, "ticketQuery/ticket_query.html",{'form':form})
