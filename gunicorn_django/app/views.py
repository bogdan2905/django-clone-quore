# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Question, Session
from .forms import Login


def index(request):
    latest = Question.objects.order_by('id').all()[:10]
    user = request.user
    print(user)
    return render(request, 'main.html', context={'latest': latest, 'user': user})


def login(request):
    if request.user:
        return HttpResponseRedirect('/app')
    errors = ''
    if request.method == 'POST':
        user_login = request.POST.get('login')
        password = request.POST.get('password')
        session_id = Session.do_session(user_login, password)

        if session_id:
            response = HttpResponseRedirect('/app/')
            response.set_cookie(key='session_id', value=session_id,
                                httponly=True,
                                expires=datetime.now() + timedelta(days=2))
            return response
        else:
            errors = 'Неверный логин/пароль'

    form = Login()
    return render(request, 'login.html', {'errors': errors, 'form': form})
