from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
import datetime
from django.contrib.auth import logout
from django.contrib import messages
from .forms import *
import json
from django.views.decorators.csrf import csrf_exempt
def sign_up(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        print(bool(form.is_valid))
        # print(form.cleaned_data['password1'])
        # print(form.cleaned_data['username'])
        # print(bool(form.cleaned_data['is_manager']))
        if form.is_valid():
            form.save()
            print('Naman')
            print(form.cleaned_data['username'])
            messages.success(request,'Account created')
            return redirect('/user/login')
        else:
            return redirect('/user/sign_up')
    else:
        form=RegistrationForm()
        context={'form':form}
        return render(request,'login/sign_up.html',context)
