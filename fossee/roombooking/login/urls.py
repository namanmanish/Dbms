from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView

app_name = 'login'
urlpatterns = [
    path('sign_up',sign_up , name="sign_up"),
    path('login', LoginView.as_view(template_name='login/login.html'), name="login"),
]