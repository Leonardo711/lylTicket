from django import forms
from django.forms import  inlineformset_factory
from trainManage.models import Station

class TicketQueryForm(forms.Form):
#    def __init__(self):
#        super(TicketQueryForm,self).__init__()
#        self.fields['startStation'].choices = ['--------'] +\
#            [station.station_name for station in Station.objects.all()]
#        self.fields['endStation'].choices = ['--------'] +\
#            [station.station_name for station in Station.objects.all()]
#    startStation = forms.ChoiceField(choices=(), required=True, widget=forms.Select())
#    endStation = forms.ChoiceField(choices=(), required=True, widget=forms.Select())
    startStation = forms.ModelChoiceField(queryset=Station.objects.all(), required=True)
    endStation = forms.ModelChoiceField(queryset=Station.objects.all(), required=True)
    date = forms.DateField(required=True, widget=forms.DateInput())


class QueryResultForm(forms.Form):
    startStation = forms.ModelChoiceField(queryset=Station.objects.all(), required=True)
    endStation = forms.ModelChoiceField(queryset=Station.objects.all(), required=True)
    date = forms.DateField(required=True, widget=forms.DateInput())


