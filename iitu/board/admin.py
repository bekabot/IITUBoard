from django.contrib import admin

from .models import Record, User, UserAdmin, FCMToken

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Record)
