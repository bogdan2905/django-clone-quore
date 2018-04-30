from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from .models import Question, Answer
from .forms import CreateQuestion, CreateAnswer
from .view_answer import answer


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
    if request.method == "POST":
        resp = answer(request)
        if resp:
            return resp
    try:
        question = Question.objects.get(id=id_question)
        answer_form = CreateAnswer()
        try:
            answers = Answer.objects.filter(question=question).all()
        except Answer.DoesNotExist:
            answers = []

        return render(request, 'question.html', {'question': question,
                                                 'answers': answers,
                                                 'count_answer': len(answers),
                                                 'answer': answer_form})
    except Question.DoesNotExist:
        return Http404
