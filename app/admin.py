# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Answer, Question, User
import hashlib

# Register your models here.

admin.site.register(Answer)
admin.site.register(Question)


class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        password = form.cleaned_data['password']
        obj.password = hashlib.md5(password.encode()).hexdigest()
        obj.save()


admin.site.register(User, UserAdmin)
