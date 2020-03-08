from django.contrib import admin

from .models import Record
from .models import User

# Register your models here.
admin.site.register(Record)
admin.site.register(User)
