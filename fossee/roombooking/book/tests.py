from django.test import SimpleTestCase,TestCase,Client
import json
from django.urls import resolve,reverse
from .views import *
from login.models import *
from .models import *
from django.contrib.auth import authenticate
from .forms import *
import requests

class Testurls(SimpleTestCase):
    
    def test_home(self):
        self.assertEquals(resolve('/book/').func,home)

    def test_book(self):
        self.assertEquals(resolve('/book/new/booking').func,book)

    def test_slot(self):
        self.assertEquals(resolve('/book/new/slot').func,slot)

    def test_cancle(self):
        self.assertEquals(resolve('/book/1').func,cancle)

    def test_edit(self):
        self.assertEquals(resolve('/book/edit/1').func,edit)

class TestView(TestCase):
    
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create(username='testuser', is_manager=True)
        self.user.set_password('12345')
        self.user1 = User.objects.create(username='testuser1', is_manager=False)
        self.user1.set_password('12345')
    
    def test_home_get(self):
        self.user.save()
        login = self.client.login(username='testuser', password='12345')
        response=self.client.get('/book/')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'book/m_home.html')

    def test_home_manager(self):
        self.user1.save()
        login = self.client.login(username='testuser1', password='12345')
        response=self.client.get('/book/')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'book/home.html')

    def test_post(self):
        self.user.save()
        login = self.client.login(username='testuser', password='12345')
        print("Sussecssfully"+str(login))
        x={'ini_time':"1:00:00",'end_time':"5:00:00"}
        response=self.client.post('/book/new/slot',x)
        self.assertEquals(response.status_code,302)
        self.assertEquals(len(Time_slots.objects.all()),1)

class Testform(SimpleTestCase):

    def test_valid(self):
        data={'ini_time':"1:00:00",'end_time':"5:00:00"}
        form=time_slot_form(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        data={}
        form=time_slot_form(data=data)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)

class Testapi(TestCase):
    
    def test_api_get(self):
        response=self.client.get('/book/api')
        self.assertEquals(response.status_code,200)

    def test_api_post(self):
        url = '/book/api'
        x={'int_time':"8:00:00",'end_time':"10:00:00"}
        response = self.client.post(url,json.dumps(x),content_type="application/json")
        self.assertEquals(response.status_code,200)
        self.assertEquals(len(Time_slots.objects.all()),1)

