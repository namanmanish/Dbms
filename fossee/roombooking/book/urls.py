from django.urls import path
from .views import *


app_name = 'book'
urlpatterns = [
    path('new/slot', slot, name="slot"),
]