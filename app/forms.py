from django import forms
from .models import Question, User
import hashlib
from django.core.exceptions import ValidationError


class Login(forms.Form):
    login = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        clean_password = self.cleaned_data['password']
        hash_password = hashlib.md5(clean_password.encode()).hexdigest()
        User.objects.create(login=self.cleaned_data['login'],
                            password=hash_password)


class Register(Login):
    second_password = forms.CharField(widget=forms.PasswordInput)

    def clean_second_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['second_password']:
            raise ValidationError('different password')
        return self.cleaned_data['second_password']

    def clean_login(self):
        try:
            User.objects.get(login=self.cleaned_data['login'])
            raise ValidationError('username is already taken')
        except User.DoesNotExist:
            return self.cleaned_data['login']


class CreateQuestion(forms.Form):
    description = forms.CharField(max_length=400)
    text = forms.CharField(widget=forms.Textarea)

    def save(self, user):
        author = User.objects.get(login=user)
        question = Question.objects.create(description=self.cleaned_data['description'],
                                           text=self.cleaned_data['text'],
                                           author=author)
        return question
