from django.db import models
from login.models import User
# Create your models here.

class Room(models.Model):
    name=models.CharField(max_length=24)
    def __str__(self):
        return self.name

class Time_slots(models.Model):
    int_time=models.TimeField()
    end_time=models.TimeField()

class Bookings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    slot_id=models.ForeignKey(Time_slots,on_delete=models.CASCADE)
    date=models.DateField(null=True,default=None)
    room=models.ForeignKey(Room,on_delete=models.CASCADE,null=True,default=None)

class dependent(models.Model):
    date=models.DateField()
    time_slot=models.ForeignKey(Time_slots,on_delete=models.CASCADE)

class advance(models.Model):
    no_days=models.IntegerField()
    

