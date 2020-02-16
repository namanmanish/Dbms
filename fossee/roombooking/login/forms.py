from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

TRUE_FALSE_CHOICES = (
    (True, 'Room manager'),
    (False, 'Customer')
)

class RegistrationForm(UserCreationForm):
    is_manager=forms.ChoiceField(choices = TRUE_FALSE_CHOICES)
    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.is_manager = self.cleaned_data['is_manager']

        if commit:
            user.save()

        return user
