from django.contrib import admin

from .models import Record, User, UserAdmin, RecordAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Record, RecordAdmin)
