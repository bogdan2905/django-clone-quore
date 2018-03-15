# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from .models import Question


def index(request):
    latest = Question.objects.order_by('-pub_date').all()[:10]
    user = request.my_app_user
    return render(request, 'main.html', context={'latest': latest, 'user': user})




