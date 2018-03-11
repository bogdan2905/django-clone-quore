# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.db import models
from hashlib import md5
import uuid


class User(models.Model):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.login

    @staticmethod
    def valid_user(login, hash_password):
        try:
            user = User.objects.get(login=login, password=hash_password)
            return user
        except User.DoesNotExist:
            return None


class Question(models.Model):
    description = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_url(self):
        return "/app/ask/question/{}/".format(self.id)


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True)
    date = models.DateField()

    @staticmethod
    def unique_key(key):
        try:
            session = Session.objects.get(key=key)
            return session
        except Session.DoesNotExist:
            return None

    @staticmethod
    def do_session(user, password):
        hash_password = md5(password.encode()).hexdigest()
        user = User.valid_user(user, hash_password)

        if user:
            session_id = uuid.uuid4().hex
            if Session.unique_key(session_id) is None:
                Session.objects.create(user=user, key=session_id,
                                       date=datetime.now() + timedelta(days=2))
                return session_id
        else:
            return None
