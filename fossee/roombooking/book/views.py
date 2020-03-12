from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
import datetime
from datetime import date
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
        x=datetime.datetime.now().date()+datetime.timedelta(days=advance.objects.get(pk=1).no_days)
        context={'form':form,'x':x}
        return render(request,'book/slot_form.html',context)

def date(i):
    return i.date

def home(request):
    if not request.user.is_manager:
        booking1=Bookings.objects.all()
        booking1=sorted(booking1,key=date,reverse=True)
        for i in booking1:
            print(i.date)
        booking=[]
        for i in booking1:
            if i.user==request.user:
                booking.append(i)
        a=[]
        b=""
        for x in booking:
            b=b+str(x.room.name)+"  "
            b=b+str((x.date.strftime('%A %d %B %Y')))+"  "
            b=b+str(x.slot_id.int_time)
            b=b+"  To  "+str(x.slot_id.end_time)
            a.append((b,x.pk,bool(datetime.datetime.combine(x.date,x.slot_id.int_time)>datetime.datetime.now())))
            b=""
        print(a)
        contex={'a':a}
        return render(request,'book/home.html',contex)
    else:
        date1=datetime.datetime.now().date()
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
                booking=[i.room for i in Bookings.objects.filter(date=date).filter(slot_id=time_slot)]
                for i in Room.objects.all():
                    if i not in booking:
                        break
                obj=Bookings.objects.create(user=request.user,date=date,slot_id=time_slot,room=i)
                obj.save()
                messages.success(request, "Slot successfully added")
                return redirect('/book/')
            else:
                print(form)
                messages.MessageFailure(request, 'Not created') 
        form=bookings_form()
        context={'form':form,'max':advance.objects.get(pk=1).no_days}
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

def desc(request):
    if request.user.is_manager:
        dep=dependent.objects.all()
        for i in range(len(dep)):
            if datetime.datetime.now().date()<(dep[i].date):
                break
        x=dependent.objects.filter(date=dep[max(i-1,0)].date)
        time=[]
        for i in x:
            time.append(i.time_slot)
        x=datetime.datetime.now().date()+datetime.timedelta(days=advance.objects.get(pk=1).no_days)
        y=1
        if datetime.datetime.now().date() in [z.date for z in dep]:
            y=0
        context={'time':time,'date1':datetime.datetime.now().date(),'date2':x,'y':y}
        return render(request,'book/time_slot.html',context)

def edits(request,id):
    if request.user.is_manager:
        if request.method=="POST":
            form=time_slot_form(request.POST)
            if form.is_valid():
                ini_time=form.cleaned_data["ini_time"]
                end_time=form.cleaned_data["end_time"]
                obj=Time_slots.objects.create(int_time=ini_time,end_time=end_time)
                obj.save()
                x=datetime.datetime.now().date()+datetime.timedelta(days=advance.objects.get(pk=1).no_days)
                for i in Time_slots.objects.all():
                    if not i.pk==id:
                        dependent.objects.create(date=x,time_slot=i).save()
                messages.success(request, "Slot successfully added")
                return redirect('/book/edit/slots')
        slot=Time_slots.objects.get(pk=id)
        x=datetime.datetime.now().date()+datetime.timedelta(days=advance.objects.get(pk=1).no_days)
        print(x)
        form=time_slot_form()
        context={'form':form,'x':x,'in':slot.int_time,'out':slot.end_time}
        return render(request,'book/slot_form.html',context)
        
def cancles(request,id):
    x1=datetime.datetime.now().date()+datetime.timedelta(days=advance.objects.get(pk=1).no_days)
    dep=dependent.objects.all()
    for i in range(len(dep)):
        if datetime.datetime.now().date()<(dep[i].date):
            break
    y=dependent.objects.filter(date=dep[max(i-1,0)].date)
    for i in y:
        if not i.time_slot.pk==id:
            dependent.objects.create(date=x1,time_slot=i.time_slot).save()
    return redirect('/book/edit/slots')

def ajaxs(request):
    date=request.GET.get('date')
    print(date)
    dep=dependent.objects.all()
    print(dep[0].date)
    for i in range(len(dep)):
        if str(date)<str(dep[i].date):
            break
    x=dependent.objects.filter(date=dep[max(i-1,0)].date)
    a=[]
    b=[]
    for i in x:
        b.append(i.time_slot.int_time)
        b.append(i.time_slot.end_time)
        b.append(i.time_slot.pk)
        a.append(b)
        b=[]
    print(a)
    context={'a':a}
    return JsonResponse(context)

def add_room(request):
    if request.user.is_manager:
        if request.method=="POST":
            form=room_form(request.POST)
            if form.is_valid():
                name=form.cleaned_data["name"]
                Room.objects.create(name=name).save()
                return redirect('/book/')
        form=room_form()
        contex={'form':form}
        return render(request,'book/add_room.html',contex)
    else:
        return HttpResponse('<h1>Customer</h1>')

def change_days(request):
    if request.user.is_manager:
        if request.method=="POST":
            form=max_d(request.POST)
            if form.is_valid():
                days=form.cleaned_data["days"]
                obj=advance.objects.get(pk=1)
                obj.no_days=days
                obj.save()
                return redirect('/book/')
        form=max_d()
        contex={'form':form,'days':advance.objects.get(pk=1).no_days}
        return render(request,'book/change_days.html',contex)
    else:
        return HttpResponse('<h1>Customer</h1>')


@csrf_exempt 
def slot_api(request):
    if request.method=="POST":
        print(request.body)
        data=request.body.decode('utf-8')
        received_json_data = json.loads(data)
        time1=received_json_data["int_time"]
        time2=received_json_data["end_time"]
        x=Time_slots.objects.create(int_time=time1,end_time=time2)
        x.save()
        return JsonResponse({'begin':x.int_time,'end':x.end_time})
    else:
        data=Time_slots.objects.all()
        a=[]
        b={}
        for i in data:
            b["start"]=i.int_time
            b["end"]=i.end_time
            a.append(b)
            b={}
        return JsonResponse({'a':a})
