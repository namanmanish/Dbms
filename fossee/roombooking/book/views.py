from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib import messages
from django.shortcuts import redirect


def slot(request):
    if not request.user.is_manager:
        return HttpResponse('<h1>Customer</h1>')
    else:
        if request.method=="POST":
            form=time_slot_form(request.POST)
            if form.is_valid():
                room=form.cleaned_data["room"]
                date=form.cleaned_data["date"]
                ini_time=form.cleaned_data["ini_time"]
                end_time=form.cleaned_data["end_time"]
                obj=time_slots.objects.create(room_id=Room.objects.get(pk=room),date=date,int_time=ini_time,end_time=end_time)
                obj.save()
                messages.success(request, "Slot successfully added")
                return redirect('')
            else:
                messages.MessageFailure(request, 'Not created')  
        form=time_slot_form()
        context={'form':form}
        return render(request,'book/slot_form.html',context)

