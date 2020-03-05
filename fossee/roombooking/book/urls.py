from django.urls import path
from .views import *
from . import views

app_name = 'book'
urlpatterns = [
    path('new/slot', slot, name="slot"),
    path('',home,name="home"),
    path('new/booking',book,name="book"),
    path('<int:id>', views.cancle,name='cancle'),
    path('edit/<int:id>',views.edit),
    path('ajax',views.ajax),
]