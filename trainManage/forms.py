from django import forms
from .models import Train, Run, Station, Seat, Carriage
from django.forms import  inlineformset_factory

class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = (
                'train_id', 
               # 'distance',
                )
        widgets={
                'train_id': forms.TextInput(attrs={'class':'form-control'}),
                }

class trainFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput())

#class RunForm(forms.ModelForm):
#    station_name = forms.CharField(max_length=20)
#    class Meta:
#        model = Run
#        fields = (
#                'station_name',
#               # 'order_of_station',
#                'arrive_time',
#                'distance_count',
#                )
#
#    def clean(self):
#        cleaned_data = self.cleaned_data
#        station_name = cleaned_data.get("station_name")
#        cleaned_data['station_name'] = Station.objects.get(station_name=station_name)
#        return cleaned_data
#
#class CustomInlineFormSetForRunForm(BaseInlineFormSet):
#    def clean(self):
#        super(CustomInlineFormSetForRunForm, self).clean()
#        for form in self.forms:
#            cleaned_data = forms.cleaned_data
#        station_name = cleaned_data.get("station_name")
#        cleaned_data['station_name'] = Station.objects.get(station_name=station_name)
#        return cleaned_data


RunForm_stationSet = inlineformset_factory(Train, 
        Run,
        fields=('order_of_station', 'station_name', 'arrive_time', 'distance_count'),
        extra=1,
        max_num= 10,
        widgets={'order_of_station':forms.TextInput(attrs={'readonly':'readonly'}),
                 'arrive_time':forms.TimeInput()},
#        formset=CustomInlineFormSetForRunForm
        )

CarriageForm = inlineformset_factory(Train,
                                 Carriage,
                                 fields=('carriage_id', 'num_seat', 'seat_type'),
                                 extra =1,
                                 max_num=20,
                                 widgets={'carriage_id':forms.TextInput(attrs={"readonly":"readonly"})},
                                 )
