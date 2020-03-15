from django.db import models


class Record(models.Model):
    record_title = models.TextField(max_length=100, verbose_name="Заголовок", default="")
    record_body = models.TextField(max_length=10000, verbose_name="Текст", default="")
    image1 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка1")
    image2 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка2")
    image3 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка3")

    def __str__(self):
        return self.record_title


class User(models.Model):
    login = models.CharField(max_length=20, verbose_name="Логин")
    password = models.CharField(max_length=30, verbose_name="Пароль")
    email = models.CharField(max_length=30, verbose_name="Email")
    token = models.CharField(max_length=100, verbose_name="Токен", default='')
    is_active = models.BooleanField(verbose_name="Активный")

    def __str__(self):
        return self.login
