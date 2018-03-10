from django.conf.urls import url
from .views import index, login

urlpatterns = [
    url(r'^$', index, name='question'),
    url(r'^login/$', login)
]