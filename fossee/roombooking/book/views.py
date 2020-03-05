from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
import datetime
from datetime import date
from django.http import JsonResponse

number_days=10  #Number of days prior which the booking can be done

def slot(request):
    if not request.user.is_manager:
        return HttpResponse('<h1>Customer</h1>')
    else:
        if request.method=="POST":
            form=time_slot_form(request.POST)
            if form.is_valid():
                ini_time=form.cleaned_data["ini_time"]
                end_time=form.cleaned_data["end_time"]
                obj=Time_slots.objects.create(int_time=ini_time,end_time=end_time)
                obj.save()
                messages.success(request, "Slot successfully added")
                return redirect('/book/')
            else:
                messages.MessageFailure(request, 'Not created')  
        form=time_slot_form()
        x=datetime.datetime.now().date()+datetime.timedelta(days=number_days)
        print(x)
        context={'form':form,'x':x}
        return render(request,'book/slot_form.html',context)

def home(request):
    if not request.user.is_manager:
        booking=Bookings.objects.filter(user=request.user)
        for i in booking:
            print(i.slot_id.end_time)
        print(request.user.username)
        a=[]
        b=""
        for x in booking:
            b=b+str(x.room.name)+" "
            b=b+str((x.date))+"  "
            b=b+str(x.slot_id.int_time)
            b=b+"  To  "+str(x.slot_id.end_time)
            a.append((b,x.pk,bool(datetime.datetime.combine(x.date,x.slot_id.int_time)>datetime.datetime.now())))
            b=""
        print(a)
        contex={'a':a}
        return render(request,'book/home.html',contex)
    else:
        date1=date.today()
        x=Bookings.objects.filter(date=date1)
        a=[]
        b={}
        c=[]
        for i in x:   
            b["roomname"]=str(i.room.name)
            b["status"]="Booked"
            b["intt"]=str(i.slot_id.int_time)
            b["endt"]=str(i.slot_id.end_time)
            b["user"]=str(i.user)
            a.append(b)
            b={}
        for i in Room.objects.all():
            if i not in [z.room for z in x]:
                b["roomname"]=str(i.name)
                b["status"]="Vaccant"
                c.append(b)
                b={}
        context={'a':a,'c':c,'date1':date1}
        return render(request,'book/m_home.html',context)


def book(request):
    if not request.user.is_manager:
        if request.method=="POST":
            form=bookings_form(request.POST)
            if form.is_valid():
                date=form.cleaned_data["date"]
                time_slot=Time_slots.objects.get(pk=form.cleaned_data["time_slot"])
                booking=Bookings.objects.filter(date=date).filter(slot_id=time_slot).room
                for i in Room.objects.all():
                    if i not in booking:
                        break
                obj=Bookings.objects.create(user=request.user,date=date,slot_id=time_slot,room=i)
                obj.save()
                messages.success(request, "Slot successfully added")
                redirect('/book/')
            else:
                messages.MessageFailure(request, 'Not created') 
        form=bookings_form()
        context={'form':form}
        return render(request,'book/book_form.html',context)
    else:
        return HttpResponse('<h1>Manager</h1>')

def edit(request,id):
    if not request.user.is_manager:
        if request.method=="POST":
           form=bookings_form(request.POST)
           print("hi")
           if form.is_valid():
                print("hi")
                date=form.cleaned_data["date"]
                time_slot=Time_slots.objects.get(pk=form.cleaned_data["time_slot"])
                booking=[i.room for i in Bookings.objects.filter(date=date).filter(slot_id=time_slot)]
                Bookings.objects.get(pk=id).delete()
                for i in Room.objects.all():
                    if i not in booking:
                        break
                obj=Bookings.objects.create(user=request.user,date=date,slot_id=time_slot,room=i)
                obj.save()
                messages.success(request, "Slot successfully added")
                return redirect('/book/')
        booking=Bookings.objects.get(pk=id)
        print(booking.slot_id.pk)
        form=bookings_form(initial={'time_slot':booking.slot_id.pk,'date':booking.date})
        contest={'form':form}
        return render(request,'book/book_form.html',contest)
        
def cancle(request,id):
    if not request.user.is_manager:
        boooking=Bookings.objects.get(pk=id)
        boooking.delete()
        return redirect('/book/')
    else:
        return HttpResponse('<h1>Manager</h1>')

def ajax(request):
    print("Hi")
    date=request.GET.get('date')
    x=Bookings.objects.filter(date=date)
    a=[]
    b=[]
    for i in x:   
        b.append(str(i.room.name))
        b.append("Booked")
        b.append(str(i.slot_id.int_time))
        b.append(str(i.slot_id.end_time))
        b.append(str(i.user))
        a.append(b)
        b=[]
    for i in Room.objects.all():
        if i not in [z.room for z in x]:
            b.append(str(i.name))
            b.append("Vaccant")
            for y in range(3):
                b.append("NA")
            a.append(b)
            b=[]
    context={'a':a}
    return JsonResponse(context)


