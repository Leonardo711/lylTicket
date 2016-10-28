from django import forms
from .models import Train, Run, Station

class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = (
                'train_id', 
               # 'distance',
                )
        widgets={
                'train_id': forms.TextInput(attrs={'class':'form-control',}),
                }

class RunForm(forms.ModelForm):
    station_name = forms.CharField(max_length=20)
    class Meta:
        model = Run
        fields = (
                'station_name',
               # 'order_of_station',
                'arrive_time',
                'distance_count',
                )

    def clean(self):
        cleaned_data = self.cleaned_data
        station_name = cleaned_data.get("station_name")
        cleaned_data['station_name'] = Station.objects.get(station_name=station_name)
        return cleaned_data




