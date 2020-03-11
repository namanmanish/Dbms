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
    path('edit/slots',views.desc),
    path('edit/slot/<int:id>',views.edits),
    path('ajax',views.ajax),
    path('ajax/slot',views.ajaxs),
    path('cancle/<int:id>',views.cancles),
    path('api',views.slot_api),
    path('new/room',views.add_room),
    path('change',views.change_days),
]