import os

from django.contrib import admin
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django_unixdatetimefield import UnixDateTimeField
from pyfcm import FCMNotification

RECORD_TYPE_CHOICES = (
    ('news', 'Новость'),
    ('ads', 'Объявление'),
    ('vacancy', 'Вакансия'),
)

ADS_CATEGORY = (
    ('services', 'Услуги'),
    ('study', 'Учеба'),
    ('lost_and_found', 'Бюро находок',),
    ('sport', 'Спорт',),
    ('hobby', 'Хобби',),
    ('sells', 'Продам',),
    ('exchange_free', 'Обмен/Отдам даром',),
    ('rent', 'Аренда жилья',),
    ('mate_search', 'Поиск соседа',),
)


class Record(models.Model):
    record_title = models.TextField(max_length=200, verbose_name="Заголовок", default="")
    record_body = models.TextField(max_length=10000, verbose_name="Текст", default="")
    image1 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка1 (не обязательно)")
    image2 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка2 (не обязательно)")
    image3 = models.ImageField(blank=True, upload_to="images", verbose_name="Картинка3 (не обязательно)")
    phone = models.CharField(blank=True, max_length=11, verbose_name="Контактный телефон (не обязательно)")
    email = models.CharField(blank=True, max_length=40, verbose_name="Контактный email (не обязательно)")
    whatsapp = models.CharField(blank=True, max_length=11, verbose_name="WhatsApp (не обяза тельно)")
    telegram = models.CharField(blank=True, max_length=30, verbose_name="Telegram логин (не обязательно)")
    record_type = models.CharField(choices=RECORD_TYPE_CHOICES, max_length=7, default='news', verbose_name="Тип записи")
    ads_category = models.CharField(blank=True, choices=ADS_CATEGORY, max_length=20,
                                    verbose_name="Категория (только для объявлений)")
    created_at = UnixDateTimeField(auto_now_add=True, blank=True)
    author = models.CharField(default="admin", max_length=100, verbose_name="Автор")
    author_email = models.CharField(blank=True, max_length=40)

    def __str__(self):
        if len(self.record_title) < 70:
            return self.record_title
        else:
            return self.record_title[0: 69] + '...'


class RecordAdmin(admin.ModelAdmin):
    exclude = ("created_at", "author", "author_email")
    list_display = ('record_title', 'record_type', 'author')


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
        push_service = FCMNotification(api_key=os.getenv('FCM_API_KEY'))

        author_email = instance.author_email
        all_tokens = FCMToken.objects.exclude(email=author_email).values_list('fcm_token', flat=True).distinct()
        list_tokens = list(all_tokens)

        if len(instance.record_title) < 40:
            push_title = instance.record_title
        else:
            push_title = instance.record_title[0: 40] + '...'

        if len(instance.record_body) < 150:
            push_body = instance.record_body
        else:
            push_body = instance.record_body[0: 150] + '...'

        data_message = {
            "title": push_title,
            "body": push_body,
            "id": instance.id,
            "type": instance.record_type
        }

        push_service.multiple_devices_data_message(registration_ids=list_tokens,
                                                   data_message=data_message)


class FCMToken(models.Model):
    email = models.CharField(max_length=100)
    fcm_token = models.CharField(max_length=1000)
