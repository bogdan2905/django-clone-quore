from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from .models import Question
from .forms import CreateQuestion


def create_question(request):
    if request.method == 'POST':

        form = CreateQuestion(request.POST)

        if form.is_valid():
            question = form.save(request.my_app_user)
            url = question.get_url()
            return HttpResponseRedirect(url)
    elif request.my_app_user:
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
