from django.db import models
from login.models import User
# Create your models here.

class Room(models.Model):
    name=models.CharField(max_length=24)
    def __str__(self):
        return self.name

class time_slots(models.Model):
    room_id=models.ForeignKey(Room,on_delete=models.CASCADE)
    date=models.DateField()
    int_time=models.TimeField()
    end_time=models.TimeField()

class Bookings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    slot_id=models.ForeignKey(time_slots,on_delete=models.CASCADE)


    

