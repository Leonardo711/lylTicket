from django import forms
from django.forms import  inlineformset_factory,modelformset_factory,formset_factory
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


#class PassengerInfoForm(forms.Form):


class PassengerInfoForm(forms.Form):
    order = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly', 'value':1}))
    seat_type = forms.CharField()
    student = forms.IntegerField()
    passenger_name = forms.CharField()
    passenger_id = forms.CharField()
    passenger_phone = forms.CharField()
    
PassengerInfoFormSet = formset_factory(PassengerInfoForm,max_num=10,extra=1)