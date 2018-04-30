from .models import Answer
from .forms import CreateAnswer
from django.shortcuts import render, HttpResponseRedirect


def answer(request):
    if request.method == "POST" and request.my_app_user:
        answer = CreateAnswer(request.POST)
        if answer.is_valid():
            answer.save(request.my_app_user)
    else:
        return HttpResponseRedirect('/login')
