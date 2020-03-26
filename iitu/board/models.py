from django.contrib import admin
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

RECORD_TYPE_CHOICES = (
    ('news', 'Новость'),
    ('ads', 'Объявление'),
    ('vacancy', 'Вакансия'),
)

ADS_CATEGORY = (
    ('sport', 'Спорт'),
    ('it', 'IT'),
    ('study', 'Учеба',),
    ('others', 'Прочее',),
)


class Record(models.Model):
    record_title = models.TextField(max_length=200, verbose_name="Заголовок", default="")
    record_body = models.TextField(max_length=10000, verbose_name="Текст", default="")
    image1 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка1")
    image2 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка2")
    image3 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка3")
    phone = models.CharField(blank=True, max_length=11, verbose_name="Контактный телефон (не обязательно)")
    email = models.CharField(blank=True, max_length=40, verbose_name="Контактный email (не обязательно)")
    whatsapp = models.CharField(blank=True, max_length=11, verbose_name="WhatsApp (не обяза тельно)")
    instagram = models.CharField(blank=True, max_length=30, verbose_name="Instagram логин (не обязательно)")
    vk = models.CharField(blank=True, max_length=30, verbose_name="VK логин/id (не обязательно)")
    telegram = models.CharField(blank=True, max_length=30, verbose_name="Telegram логин (не обязательно)")
    record_type = models.CharField(choices=RECORD_TYPE_CHOICES, max_length=7, default='news', verbose_name="Тип записи")
    ads_category = models.CharField(blank=True, choices=ADS_CATEGORY, max_length=20,
                                    verbose_name="Категория (только для новостей)")

    def __str__(self):
        if len(self.record_title) < 70:
            return self.record_title
        else:
            return self.record_title[0: 69] + '...'


class User(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя")
    surname = models.CharField(max_length=20, verbose_name="Фамилия")
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=30, verbose_name="Email")
    token = models.CharField(max_length=100, default='')
    is_active = models.BooleanField(verbose_name="Активный")

    def __str__(self):
        return self.name + ' ' + self.surname


class UserAdmin(admin.ModelAdmin):
    exclude = ('password', "token")


@receiver(signals.post_save, sender=Record)
def create_record(sender, instance, created, **kwargs):
    if created:
        print("New record created " + instance.record_title)
