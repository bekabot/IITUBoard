from django.db import models
import json


class Record(models.Model):
    text = models.CharField(max_length=2000, verbose_name="Введите текст")

    def __str__(self):
        return self.text


class User(models.Model):
    login = models.CharField(max_length=20, verbose_name="Логин")
    password = models.CharField(max_length=30, verbose_name="Пароль")
    email = models.CharField(max_length=30, verbose_name="Email")
    token = models.CharField(max_length=100, verbose_name="Токен", default='')
    is_active = models.BooleanField(verbose_name="Активный")

    def __str__(self):
        return self.login

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
