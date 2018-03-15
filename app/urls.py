from django.conf.urls import url
from .views import index
from .views_account import login, logout, create_account
from .views_questions import create_question, show_question


urlpatterns = [
    url(r'^$', index, name='question'),
    url(r'^login/$', login),
    url(r'^exit/$', logout),
    url(r'^ask/$', create_question),
    url(r'^ask/question/(\d+)', show_question),
    url(r'^create-account/$', create_account)
]
