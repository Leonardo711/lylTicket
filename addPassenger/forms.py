#-*- coding:utf-8 -*-
from django import forms
from .models import *
from django.forms import modelformset_factory,formset_factory
from django.contrib.auth.models import User


class PassengerForm(forms.Form):
	order = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly', 'value':1}))
	passenger_name = forms.CharField()
	passenger_id = forms.CharField()
	student = forms.IntegerField()

	
PassengerFormSet = formset_factory(PassengerForm,max_num=10)


'''
class PassengerForm(forms.ModelForm):
	class Meta:
		model = Passenger
		fields = '__all__'


PassengerFormSet = modelformset_factory(Passenger,PassengerForm,max_num=10)
'''