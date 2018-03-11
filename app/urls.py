from django.conf.urls import url
from .views import index, login, logout, create_question, show_question

urlpatterns = [
    url(r'^$', index, name='question'),
    url(r'^login/$', login),
    url(r'^exit/$', logout),
    url(r'^ask/$', create_question),
    url(r'^ask/question/(\d+)', show_question)
]
