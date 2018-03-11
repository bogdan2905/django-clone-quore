# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from .models import Question, Session
from .forms import Login, CreateQuestion


def index(request):
    latest = Question.objects.order_by('-id').all()[:10]
    user = request.user
    return render(request, 'main.html', context={'latest': latest, 'user': user})


def login(request):
    if request.user:
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


def create_question(request):
    if request.method == 'POST':

        form = CreateQuestion(request.POST)

        if form.is_valid():
            question = form.save(request.user)
            url = question.get_url()
            return HttpResponseRedirect(url)
    elif request.user:
        form = CreateQuestion()
    else:
        return HttpResponseRedirect('/login')
    return render(request, 'ask.html', {'form': form})


def show_question(request, id_question):
    try:
        question = Question.objects.get(id=id_question)
        return render(request, 'question.html', {'question': question})
    except Question.DoesNotExist:
        return Http404
