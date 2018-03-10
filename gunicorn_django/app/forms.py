from django import forms
from .models import User


class Login(forms.Form):
    login = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

