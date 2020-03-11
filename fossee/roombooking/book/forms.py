from django import forms
from .models import *

class time_slot_form(forms.Form):
    ini_time=forms.TimeField()
    end_time=forms.TimeField()


class bookings_form(forms.Form):
    MY_CHOICES=()
    x=Time_slots.objects.all()
    for i in x:
        MY_CHOICES += ((i.pk, str(i.int_time)+' -- '+str(i.end_time)),)
    date=forms.DateField()
    time_slot=forms.ChoiceField(choices=MY_CHOICES)


class room_form(forms.Form):
    name=forms.CharField(max_length=25)


class max_d(forms.Form):
    days=forms.IntegerField()
