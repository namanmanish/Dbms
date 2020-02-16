from django import forms
from .models import *

class time_slot_form(forms.Form):
    MY_CHOICES=()
    x=len(Room.objects.all())
    for i in range(x):
        MY_CHOICES += ((i+1, str(Room.objects.get(pk=i+1).name)),)
    room=forms.ChoiceField(choices=MY_CHOICES)
    date=forms.DateField()
    ini_time=forms.TimeField()
    end_time=forms.TimeField()
