from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from .models import Session
from .forms import Login, Register


def login(request):
    if request.my_app_user:
        return HttpResponseRedirect('/')
    errors = ''
    if request.method == 'POST':
        user_login = request.POST.get('login')
        password = request.POST.get('password')
        session_id = Session.do_session(user_login, password)

        if session_id:
            response = HttpResponseRedirect('/')
            response.set_cookie(key='session_id', value=session_id,
                                httponly=True,
                                expires=datetime.now() + timedelta(days=2))
            return response
        else:
            errors = 'Неверный логин/пароль'

    form = Login()
    return render(request, 'login.html', {'errors': errors, 'form': form})


def logout(request):
    session_id = request.COOKIES.get("session_id")
    if session_id is not None:
        Session.objects.filter(key=session_id).delete()

    return HttpResponseRedirect('/')


def create_account(request):
    if request.my_app_user:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = Register(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/login')
        form = Register()
        return render(request, 'create_account.html', {'form': form})
